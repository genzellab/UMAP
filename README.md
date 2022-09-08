Dependencies: To-add. 


# UMAP
Repository for UMAP project. 

## Main scripts: :file_folder: 

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

For filtering the aligned data use:
```
fn=2500;
Wn1=[70/(fn/2) 400/(fn/2)]; % Cutoff=70-400 Hz
[b,a] = butter(3,Wn1,'bandpass');
Y_filtered=cellfun(@(x) filtfilt(b,a,x.').' , Y,'UniformOutput',false);
```

To Z-score (per day) and organize the data in a structure with nested structures. The same script can be used for RAW ripples, just change Y_filtered for Y and RGS for RGS_raw.
:
```
Data=[];
for i=1:length(Y_filtered)
data=Y_filtered{i};
Data=[Data; data];
    
end
size(Data)
sum(cellfun('length',Y_filtered))

SD=(std(Data(:))); %Standard deviation of ripples of that day.
Z=cellfun(@(x)  (x-mean(x,2))/SD ,Y_filtered,'UniformOutput',false  );

RGS.Rat8.OD=Z; % Change this manually

clearvars -except VEH RGS
```


_**Organize data in a table:**_ 
  
  * create_table.m
 

