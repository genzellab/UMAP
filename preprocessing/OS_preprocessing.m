addpath(genpath('/home/adrian/Documents/GitHub/UMAP'))

cd /mnt/genzel/Rat/OS_UMAP_analysis/UMAP_Basic_OS/
%cd /mnt/genzel/Rat/OS_CBD_analysis/chronic

RatID=getfolder;

for i=1:length(RatID)
    cd(RatID{i})

    files = dir;
    files={files.name};
    files=files(cellfun(@(x) contains(x,'GC') & ~contains(x,'preprocessed'),files));  

    for j=1:length(files)
        load(files{j})
        %xo
         Y= cellfun(@(x) alignripples(x),GC_window_ripples_broadband_total,'UniformOutput',false);
%        Y= cellfun(@(x) alignripples(x),GC_window_ripples_total,'UniformOutput',false);
        clear GC_window_ripples_broadband_total
        clear GC_window_ripples_total
        
        fn=2500;
        Wn1=[100/(fn/2) 300/(fn/2)]; % Cutoff=100-300 Hz
        [b,a] = butter(3,Wn1,'bandpass');
        Y_filtered=cellfun(@(x) filtfilt(b,a,x.').' , Y,'UniformOutput',false); 

        [Z]=zscore_umap(Y_filtered);
        
        %xo
        save(['preprocessed2_' files{j}],'Z','-v7.3');
        clear Y Y_filtered Z
    end
    cd ..
end
