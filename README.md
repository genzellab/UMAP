Dependencies: To-add. 


# UMAP
Repository for UMAP project. 

## Main scripts: :file_folder: 

_**Data preprocessing:**_ 
  * downsample_os_basic.m : Downsamples channels to 2500 Hz.
  * downsample_rgs14_2500.m : Downsamples RGS14 detections to 2500 Hz. 
  * merge.pt5.m : Merges split files of PT5 to later send to Kopal and compute the ripple timestamps. 
  * alignripples.m : Shifts ripple traces to align them always on the minimum closest to the peak. You might encounter some dimension errors which are due to either extra samples from GC files or empty arrays. You can fix with this script:

```
Y= cellfun(@(x) alignripples(x),GC_window_ripples_total,'UniformOutput',false);
%%
i=9; %Trial number. Change this accordingly. 
ou=find((cellfun('length',GC_window_ripples_total{i})~= 15001))
%%
for j=1:length(ou)
    if isempty( GC_window_ripples_total{i}{ou(j)})
        GC_window_ripples_total{i}{ou(j)}=[];
    else
            GC_window_ripples_total{i}{ou(j)}=GC_window_ripples_total{i}{ou(j)}(:,1:15001);
    end
end
```

_**Sleep stages analysis:**_ 
  
  * filename2.m
 
_**Event detection:**_ 
  
  * filename3.m
