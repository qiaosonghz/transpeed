#include <algorithm>
#include <cmath>
#include <cstring>
#include <numeric>
#include <random>

#include "spotlight-common.hpp"
int test_gemm();
#ifdef _DEBUG_OUT
  static constexpr uint64_t num_samples = 1;
#else
  static constexpr uint64_t num_samples = 3;
#endif
static std::string logfile = "";

template<bool DumpAll>
Cost<DumpAll> evaluateHelper(
  uint64_t * shape,
  std::string const & layer_type,
  uint64_t num_pes,
  uint64_t num_simd_lanes,
  uint64_t bit_width,
  uint64_t bandwidth,
  uint64_t num_levels,
  uint64_t * buf_sizes,
  uint64_t * num_sub_clusters,
  char const * dataflow,
  uint64_t search_permutations,
  std::string logfile
)
{
  (void) num_levels;
  uint64_t dim_num = 7;
  if (layer_type == "GEMM") {
      dim_num = 3;
  }

#if (defined _DEBUG_OUT) && (defined _VERBOSE)
  std::cout << "    shape = { {";
  std::string prefix = "";


  for(uint64_t i = 0; i < dim_num; ++i) {
    std::cout << prefix << shape[i];
    prefix = ", ";
  }
  std::cout << "} };\n";

  std::cout << "    num_pes = " << num_pes << ";\n";
  std::cout << "    num_simd_lanes = " << num_simd_lanes << ";\n";
  std::cout << "    bit_width = " << bit_width << ";\n";
  std::cout << "    bandwidth = " << bandwidth << ";\n";
  std::cout << "    num_levels = " << num_levels << ";\n";

  std::cout << "    buf_sizes = { {";
  prefix = "";
  for(uint64_t i = 0; i < num_levels; ++i) {
    std::cout << prefix << buf_sizes[i];
    prefix = ", ";
  }
  std::cout << "} };\n";

  std::cout << "    num_sub_clusters = { {";
  prefix = "";
  for(uint64_t i = 0; i < num_levels; ++i) {
    std::cout << prefix << num_sub_clusters[i];
    prefix = ", ";
  }
  std::cout << "} };\n";

  std::cout << "    dataflow = \"" << dataflow << "\";\n";
#endif

  maestro::InitializeBaseObjects(0);

  Point point;
  point.num_pes = num_pes;
  point.num_simd_lanes = num_simd_lanes;
  // TODO: Make this support arbitrary levels of memory
  point.l1_size = buf_sizes[0];
  point.l2_size = buf_sizes[1];
  point.bit_width = bit_width;
  point.bw = bandwidth;
  point.latency = 1;

  size_t parse_pos = 0;
  uint64_t sub_cluster_level = 1;
  bool done = false;
  while(! done) {
    std::string dataflow_str{dataflow};
    char loop_type = dataflow_str[parse_pos];
    ++parse_pos;
    if(loop_type != 'C') {
      auto bar = dataflow_str.find('|', parse_pos);
      std::string dimension{dataflow_str, parse_pos, bar - parse_pos};
      parse_pos = bar + 1;
      auto comma = dataflow_str.find(',', parse_pos);
      std::string tile_size_str;
      if(comma == std::string::npos) {
        tile_size_str = std::string(dataflow_str, parse_pos);
        done = true;
      } else {
        tile_size_str = std::string(dataflow_str, parse_pos, comma - parse_pos);
        parse_pos = comma + 1;
      }
      // std::cout << loop_type << ' ' << dimension << ' ' << tile_size_str << '\n';
      uint64_t tile_size = std::stoi(tile_size_str);
      point.dataflow.push_back(std::make_tuple(loop_type, tile_size, dimension));
    } else {
        point.dataflow.push_back(std::make_tuple('C', num_sub_clusters[sub_cluster_level], "P"));
        // std::cout << loop_type << '\n';
        ++sub_cluster_level;
        ++parse_pos;
    }
  }

  ShapeT shape_map;
  if (layer_type == "GEMM") {
      shape_map['M'] = std::make_pair(shape[0], 1);
      shape_map['K'] = std::make_pair(shape[1], 1);
      shape_map['N'] = std::make_pair(shape[2], 1);
  } else {
      shape_map['N'] = std::make_pair(shape[0], shape[1]);
      shape_map['K'] = std::make_pair(shape[2], shape[3]);
      shape_map['C'] = std::make_pair(shape[4], shape[5]);
      shape_map['X'] = std::make_pair(shape[6], shape[7]);
      shape_map['Y'] = std::make_pair(shape[8], shape[9]);
      shape_map['R'] = std::make_pair(shape[10], shape[11]);
      shape_map['S'] = std::make_pair(shape[12], shape[13]);
  }

  std::ofstream result_file;

//

  Point best_point;
  Cost<DumpAll> best_cost;

  if(search_permutations) {
    std::array<uint64_t, 7> indices;
    std::iota(indices.begin(), indices.begin() + dim_num, 0);
//    std::iota(indices.begin(), indices.end(), 0);

    std::vector<Point> space_batch(num_samples);
    std::vector<Cost<DumpAll>> cost_batch(num_samples);

    std::random_device rd;
    std::mt19937 rng{rd()};
    for(uint64_t i = 0; i < num_samples; ++i) {
      Point copy = point;
      std::shuffle(indices.begin(), indices.begin() + dim_num, rng);

      for(uint64_t j = 0; j < dim_num; ++j) { copy.dataflow[j] = point.dataflow[indices[j]]; }

      space_batch[i] = copy;
    }

    runBatch(num_samples, shape_map, layer_type, space_batch, cost_batch, result_file, best_point, best_cost, logfile);

  } else {
    best_point = point;
    best_cost = runWrapper<DumpAll>(0, shape_map, layer_type, point, logfile);
  }

#ifdef _DEBUG_OUT
  for(auto const & elem : shape_map) {
    std::cout << elem.first << ' ' << elem.second.first << ' ' << elem.second.second << '\n';
  }
  std::cout << best_point << '\n';
  printCost(std::cout, best_cost);
#endif

  return best_cost;
}

extern "C" __attribute__((visibility("default")))
char const * evaluateWithDump(
  uint64_t * shape,
  char const * layer_type,
  uint64_t num_pes,
  uint64_t num_simd_lanes,
  uint64_t bit_width,
  uint64_t bandwidth,
  uint64_t num_levels,
  uint64_t * buf_sizes,
  uint64_t * num_sub_clusters,
  char const * dataflow,
  uint64_t search_permutations,
  char const * logfile
)
{
  Cost<true> best_cost = evaluateHelper<true>(
    shape,
    std::string{layer_type},
    num_pes,
    num_simd_lanes,
    bit_width,
    bandwidth,
    num_levels,
    buf_sizes,
    num_sub_clusters,
    dataflow,
    search_permutations,
    std::string{logfile}
  );

  std::stringstream ret_ss;
  ret_ss << "{";
  if(best_cost.valid) {
    std::string prefix = "";
    for(auto const & node : best_cost.costs) {
      if(std::isfinite(node.second)) {
        ret_ss << prefix << '"' << MetricTypeToString(node.first) << "\": " << std::to_string(node.second);
        prefix = ", ";
      }
    }
  }
  ret_ss << "}";

  std::string ret_s = ret_ss.str();
  char * ret = new char[ret_s.size() + 1];
  std::memcpy(ret, ret_s.c_str(), ret_s.size() + 1);
  return ret;
}

extern "C" __attribute__((visibility("default")))
double * evaluate(
  uint64_t * shape,
  char const * layer_type,
  uint64_t num_pes,
  uint64_t num_simd_lanes,
  uint64_t bit_width,
  uint64_t bandwidth,
  uint64_t num_levels,
  uint64_t * buf_sizes,
  uint64_t * num_sub_clusters,
  char const * dataflow,
  uint64_t search_permutations,
  char const * logfile
)
{
  Cost<false> best_cost = evaluateHelper<false>(
    shape,
    std::string{layer_type},
    num_pes,
    num_simd_lanes,
    bit_width,
    bandwidth,
    num_levels,
    buf_sizes,
    num_sub_clusters,
    dataflow,
    search_permutations,
    std::string{logfile}
  );

  double * ret = new double[5];
  if(best_cost.valid) {
    ret[0] = best_cost.delay;
    ret[1] = best_cost.energy;
    ret[2] = best_cost.area;
    ret[3] = best_cost.power;
    ret[4] = best_cost.throughput;
  } else {
    ret[0] = 0;
    ret[1] = 0;
    ret[2] = 0;
    ret[3] = 0;
    ret[4] = 0;
  }
  return ret;
}

#ifdef _WITH_MAIN
int main(int argc, char ** argv)
{
  if (argc != 3) {
    std::cout << "Usage: " << argv[0] << " config logfile\n";
    return 0;
  }

  std::string config{argv[1]};
  logfile = std::string{argv[2]};

  std::array<uint64_t, 7> shape;
  uint64_t num_pes, num_simd_lanes, bit_width, bandwidth, num_levels;
  std::array<uint64_t, 2> buf_sizes;
  std::array<uint64_t, 2> num_sub_clusters;
  std::array<uint64_t, 14> dataflow;
  char const * tile_order;

  if(config == "ours") {
    shape = { {1, 32, 1, 224, 224, 3, 3} };
    num_pes = 216;
    num_simd_lanes = 8;
    bit_width = 7;
    bandwidth = 240;
    num_levels = 2;
    buf_sizes = { {229376, 76457}};
    num_sub_clusters = { {3, 72} };
    dataflow = { {2, 1, 8, 1, 224, 3, 3, 8, 1, 2, 1, 2, 1, 3} };
    tile_order = "YNKCXRSXNKCYRS";
  } else if(config == "eyeriss") {
    shape = { {1, 32, 1, 224, 224, 3, 3} };
    num_pes = 168;
    num_simd_lanes = 1;
    bit_width = 16;
    bandwidth = 64;
    num_levels = 2;
    buf_sizes = { {384000, 365} };
    num_sub_clusters = { {14, 12} };
    dataflow = { {16, 1, 8, 1, 224, 3, 3, 1, 1, 8, 1, 1, 1, 1} };
    tile_order = "XNKCYRSXNKCYRS";
  }

  evaluate(shape.data(),
    num_pes,
    num_simd_lanes,
    bit_width,
    bandwidth,
    num_levels,
    buf_sizes.data(),
    num_sub_clusters.data(),
    dataflow.data(),
    tile_order
  );

  return 0;
}
#endif


int test_gemm()
{
//  maestro::InitializeBaseObjects(option.message_print_lv);

    std::array<uint64_t, 3> shape = {128, 512, 1536};
    const char* layer_type = "GEMM";
    uint64_t num_pes = 286;
    uint64_t num_simd_lanes = 14;
    uint64_t bit_width = 8;
    uint64_t bandwidth = 186;
    uint64_t num_levels = 2;

    std::array<uint64_t, 2> buf_sizes = {204800,172032};
    std::array<uint64_t, 2> num_sub_clusters = {1,128};
    std::string dataflow = "SN|384,TM|8,TK|512,C,SN|128,TM|8,TK|2";
    uint64_t search_permutations = 1;
    char const * logfile = "logs/ALBERT_MH_FC_DimReduce_VKQ_0.log";

    double* ret = evaluate(
            shape.data(),
            layer_type,
            num_pes,
            num_simd_lanes,
            bit_width,
            bandwidth,
            num_levels,
            buf_sizes.data(),
            num_sub_clusters.data(),
            dataflow.data(),
            search_permutations,
            logfile
    );

    for (size_t i = 0; i < 4; i++) {
        std::cout << "ret[" << i << "] = " << ret[i] << std::endl;
    }


    return 0;
}