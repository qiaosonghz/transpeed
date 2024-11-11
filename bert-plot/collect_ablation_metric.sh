
ga_path="/results/Edge/Spotlight-GA/EDP/TRANSFORMER/"
ga_gemm_files="out.txt20231115114945 out.txt20231115114950 out.txt20231115114955 out.txt20231115115000 out.txt20231115115005 out.txt20231115120147 out.txt20231115120152 out.txt20231115120157 out.txt20231115120202 out.txt20231115120207"
ga_gemm_files="out.txt20231116130530 out.txt20231116130525 out.txt20231116130540 out.txt20231116130545 out.txt20231116130535 out.txt20231116131729 out.txt20231116131724 out.txt20231116131734 out.txt20231116131744 out.txt20231116131739"


gr_path="/results/Edge/Spotlight-R/EDP/TRANSFORMER/"
gr_gemm_files="out.txt20231115123427   out.txt20231115123432   out.txt20231115123437   out.txt20231115123442   out.txt20231115123447   out.txt20231115125759   out.txt20231115125805   out.txt20231115125809   out.txt20231115125814   out.txt20231115125820"
gr_gemm_files="out.txt20231116134907 out.txt20231116134912 out.txt20231116134917 out.txt20231116134922 out.txt20231116134927 out.txt20231116135901 out.txt20231116135916 out.txt20231116135906 out.txt20231116135911 out.txt20231116135921"

gv_path="/results/Edge/Spotlight-V/EDP/TRANSFORMER/"
gv_gemm_files="out.txt20231115160327   out.txt20231115160331   out.txt20231115160337   out.txt20231115160342   out.txt20231115160349   out.txt20231115172214   out.txt20231115172219   out.txt20231115172224   out.txt20231115172231   out.txt20231115172236"
gv_gemm_files="out.txt20231116152517 out.txt20231116152512 out.txt20231116152523 out.txt20231116152528 out.txt20231116152534 out.txt20231116160330 out.txt20231116160336 out.txt20231116160353 out.txt20231116160341 out.txt20231116160347"

transpeed_path="/results/Edge/Spotlight/EDP/TRANSFORMER/"
transpeed_gemm_files="out.txt20231115223207   out.txt20231115223204   out.txt20231115223203   out.txt20231115223200   out.txt20231115223212   out.txt20231116074758   out.txt20231116074808   out.txt20231116074805   out.txt20231116074800   out.txt20231116074803"

path=$transpeed_path
files=$transpeed_gemm_files
path=$1
files=$2

first_parts=$(echo $files | awk '{last = $NF; $NF = ""; print $0}')
last_file=$(echo $files | awk '{print($NF)}')

path="/root/hourz/spotlight_dev/"$path
echo "["
for file in $first_parts
do
    grep "dump_hwpoint_for_plot" "$path/$file" | tail -n 1 | awk -F':' '{print $2}'
    echo ","
done
grep "dump_hwpoint_for_plot" "$path/$last_file" | tail -n 1 | awk -F':' '{print $2}' 
echo "]"

