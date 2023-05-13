_**Data preprocessing:**_ 
Downsampling first requires generating the corresponding .mat files with information about rat IDS, channels,etc. They can be generated using the Corticohippocampal toolbox's [GUI](https://github.com/Aleman-Z/CorticoHippocampal/tree/master/GUI). You can also follow this [video tutorial](https://www.youtube.com/watch?v=vtYHah4QgTg). 

  * downsample_os_basic.m : Downsamples channels to 2500 Hz.
  * downsample_os_nsd.m : Downsamples channels to 2500 Hz. 
  * downsample_rgs14_2500.m : Downsamples RGS14 detections to 2500 Hz. 
  * merge.pt5.m : Merges split files of PT5 to later send to Kopal and compute the ripple timestamps. 
I later used this script to check that the merged PT5's had the right ripple alignment:
```
x=GC_window_ripples_total{9}{end}(2,floor(15001/2)-500:floor(15001/2)+500);
fn=2500;
 Wn1=[100/(fn/2) 300/(fn/2)]; % Cutoff=100-300 Hz
[b,a] = butter(3,Wn1,'bandpass');
hpc_filt=filtfilt(b,a,x);
plot(hpc_filt)
hold on
stem(500,200)
```

