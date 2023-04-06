%Uncomment depending on dataset used. w
%cd /mnt/genzel/Rat/OS_UMAP_analysis/UMAP_Basic_OS/
 cd /mnt/genzel/Rat/OS_CBD_analysis/chronic
%cd /mnt/genzel/Rat/OS_Ephys_RGS14_analysis/UMAP

RatID=getfolder;

for i=1:length(RatID)
    cd(RatID{i})

    files = dir;
    files={files.name};
    files=files(cellfun(@(x) contains(x,'GC') & ~contains(x,'preprocessed') & ~contains(x,'newfeatures') ,files));  

    for j=1:length(files)
        load(files{j})
        %xo
%         Y= cellfun(@(x) alignripples(x),GC_window_ripples_broadband_total,'UniformOutput',false);
        try
            %Y= cellfun(@(x) alignripples(x),GC_window_ripples_total,'UniformOutput',false);
%            Y= cellfun(@(x) alignripples(x),GC_window_ripples_broadband_total,'UniformOutput',false);
            [rip_duration, rip_phase, SO_b, SO_a, rip_threshold]= cellfun(@(x) extra_features(x),GC_window_ripples_broadband_total,'UniformOutput',false);
%            [YY,xx]= cellfun(@(x) extra_features(x),x,'UniformOutput',false);
            
% [rip_duration, rip_phase, SO_b, SO_a rip_threshold,]=extra_features(x)
        catch
            'Dimension error, correcting it.'
            xo
             for ii=1:9
                 ou=find((cellfun('length',GC_window_ripples_total{ii})~= 15001))
                 if  ~isempty(ou)
                     
                    for jj=1:length(ou)
                        if isempty( GC_window_ripples_total{ii}{ou(jj)})
                            GC_window_ripples_total{ii}{ou(jj)}=[];
                        else
                                GC_window_ripples_total{ii}{ou(jj)}=GC_window_ripples_total{ii}{ou(jj)}(:,1:15001);
                        end
                    end                     
                     
                 end
             end
%                          Y= cellfun(@(x) alignripples(x),GC_window_ripples_total,'UniformOutput',false);
                        [rip_duration, rip_phase, SO_b, SO_a, rip_threshold]= cellfun(@(x) extra_features(x),GC_window_ripples_broadband_total,'UniformOutput',false);
        end
        clear GC_window_ripples_broadband_total
        clear GC_window_ripples_total
        
%         fn=2500;
%         Wn1=[100/(fn/2) 300/(fn/2)]; % Cutoff=100-300 Hz
%         [b,a] = butter(3,Wn1,'bandpass');
%         Y_filtered=cellfun(@(x) filtfilt(b,a,x.').' , Y,'UniformOutput',false); 

%        [Z]=zscore_umap(Y);
        
        %xo
        save(['newfeatures_' files{j}],'rip_duration', 'rip_phase', 'SO_b', 'SO_a', 'rip_threshold','-v7.3');
        clear rip_duration rip_phase SO_b SO_a rip_threshold
    end
    cd ..
end
