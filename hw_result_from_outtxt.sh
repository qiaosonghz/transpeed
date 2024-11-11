#!/bin/bash
dir1=$1
echo $dir1

#dir2=$(echo $dir1 | sed -e 's/Spotlight/Spotlight-HEBO/g' )
#dir3=$(echo $dir1 | sed -e 's/Spotlight-HEBO/Spotlight/g' )


#find $dir1 $dir2 $dir3 -type f -name 'out.txt*' | xargs -i grep hw_sample {}| awk -F'< sw_result' '{print $1}' | awk -F'target' '{print $2}' | sed 's/point/#/g' | sed 's/feats/#/g' | awk -F'#' '{print $1,"-",$2,"-",$3}'
find $dir1 -type f -name 'out.txt*' | xargs -i grep hw_sample {}| awk -F'< sw_result' '{print $1}' | awk -F'target' '{print $2}' | sed 's/point/#/g' | sed 's/feats/#/g' | awk -F'#' '{print $1,"-",$2,"-",$3}' | sed -e 's/,userdata:.*//g'
