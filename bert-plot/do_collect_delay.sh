data="
│ spotlight-v  │ delay  │ ['out.txt20231117041835','out.txt20231117041840','out.txt20231117041846','out.txt20231117041851','out.txt20231117041857','out.txt20231117045721','out.txt20231117045726','out.txt20231117045732','out.txt20231117045737','out.txt20231117045743'] │\n
│ transpeed    │ delay  │ ['out.txt20231117070737','out.txt20231117070742','out.txt20231117070748','out.txt20231117070753','out.txt20231117070759','out.txt20231117075106','out.txt20231117075111','out.txt20231117075117','out.txt20231117075122','out.txt20231117075128'] │\n
│ spotlight-r  │ delay  │ ['out.txt20231117173852','out.txt20231117173857','out.txt20231117173902','out.txt20231117173907','out.txt20231117173912','out.txt20231117181721','out.txt20231117181726','out.txt20231117181731','out.txt20231117181736','out.txt20231117181741'] │\n
│ spotlight-ga │ delay  │ ['out.txt20231117141517','out.txt20231117141522','out.txt20231117141527','out.txt20231117141532','out.txt20231117141537','out.txt20231117150609','out.txt20231117150614','out.txt20231117150619','out.txt20231117150624','out.txt20231117150629'] │\n
│ transpeed-s             │ delay  │        ['out.txt20231120090114','out.txt20231120090120','out.txt20231120090125','out.txt20231120090131','out.txt20231120090136','out.txt20231120093935','out.txt20231120093941','out.txt20231120093946','out.txt20231120093952','out.txt20231120093957'] │100 │        108732.2 │
"

## delay
ga_path="/results/Edge/Spotlight-GA/Delay/TRANSFORMER/"
ga_gemm_files=`echo $data | grep 'spotlight-ga' | awk -F'│' '{print $4}' | sed "s/','/ /g; s/\['//; s/'\]//"`



gr_path="/results/Edge/Spotlight-R/Delay/TRANSFORMER/"
### delay
gr_gemm_files=`echo $data | grep 'spotlight-r' | awk -F'│' '{print $4}' | sed "s/','/ /g; s/\['//; s/'\]//"`

#
gv_path="/results/Edge/Spotlight-V/Delay/TRANSFORMER/"
gv_gemm_files=`echo $data | grep 'spotlight-v' | awk -F'│' '{print $4}' | sed "s/','/ /g; s/\['//; s/'\]//"`


# transpeed-s
transpeed_s_path="/results/Edge/Spotlight/Delay/TRANSFORMER/"
transpeed_s_gemm_files=`echo $data | grep transpeed-s | awk -F'│' '{print $4}' | sed "s/','/ /g; s/\['//; s/'\]//"`

# transpeed
transpeed_path="/results/Edge/Spotlight-HEBO/Delay/TRANSFORMER/"
transpeed_gemm_files=`echo $data | grep transpeed | awk -F'│' '{print $4}' | sed "s/','/ /g; s/\['//; s/'\]//"`

#
#sh collect_ablation_metric.sh $ga_path "$ga_gemm_files" > ablation_ga_delay_metric1119.txt
#sh collect_ablation_metric.sh $gr_path "$gr_gemm_files" > ablation_gr_delay_metric1119.txt
#sh collect_ablation_metric.sh $gv_path "$gv_gemm_files" > ablation_gv_delay_metric1119.txt
sh collect_ablation_metric.sh $transpeed_s_path "$transpeed_s_gemm_files" > ablation_transpeed_s_delay_metric1119.txt
#sh collect_ablation_metric.sh $transpeed_path "$transpeed_gemm_files" > ablation_transpeed_delay_metric1119.txt

