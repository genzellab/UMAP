clear variables

% Add libraries to path. 
addpath(genpath('/home/adrian/Documents/GitHub/CorticoHippocampal/'));
addpath(genpath('/home/adrian/Documents/GitHub/ADRITOOLS/'));

%Load GUI's file
cd('/home/adrian/Documents/UMAP')
load('OS_RGS14_UMAP_downsampling.mat')

%Specify Rat number
Rat=7;
% cd('/home/adrian/Documents/UMAP/Ripple Timestamps RGS14 /Ripple Timestamps RGS14 ')
cd('/home/adrian/Documents/UMAP/Ripple Timestamps RGS14 /corrections_merged')


cd(num2str(Rat))

sd_folders=dir;
sd_folders={sd_folders.name};
sd_folders=sd_folders(3:end);
% rip_timestamp_folders=sd_folders;
%xo

for ind1=1:length(sd_folders)
r_time=load(sd_folders{ind1});
rip_timestamps{ind1}=r_time.ripple_timestamps;

end

sd_folders=cellfun(@(equis1) erase(equis1,'ripple_timestamps_') ,sd_folders,'UniformOutput',false);
sd_folders=cellfun(@(equis1) erase(equis1,'.mat') ,sd_folders,'UniformOutput',false);



cd('/media/adrian/GL14_RAT_FANO/Rat_OS_Ephys_RGS14_rat7_373727')
      yy = {'HPC'};       
      xx = {'PFC'};
      ss = 3;   %NREM
%% 


nr_swr_HPC = [];
nr_swr_Cortex = [];
D_all = [];
nr_cohfos_pt_animal = [];    
fs = 30000; % Raw data sampling rate. 
fs_new=2500;

nr_cohfos_pt = [];

g=sd_folders;

total_swrs=[];
total_hfos=[]; 
total_swrs_minute=[];
total_hfos_minute=[];

% ripple_phases_comp = [];
ripple_waveform_comp = [];
ripple_waveform_umap_comp = [];

% ripple_waveform_broadband_comp = [];
GC_window_ripples_comp = [];
% GC_window_ripples_broadband_comp = [];
%xo
    for j = 1:length(g)  %study day index 

        
        
        nr_cohfos_pt=zeros(1,9);
        cd(g{j})
        
        G=getfolder;
                
%%        
%Get presleep
cfold3=[];
cfold=G(or(cellfun(@(x) ~isempty(strfind(x,'pre')),G),cellfun(@(x) ~isempty(strfind(x,'Pre')),G)));
for q=1:length(cfold)
    if (~contains(cfold{q}, 'test') && ~contains(cfold{q}, 'Test'))
        cfold3=[cfold3; cfold{q}];
    end
end
if ~isempty(cfold3)
    cfold=cellstr(cfold3)';
end

% Get post trials
cfold3=[];
cfold2=G(or(cellfun(@(x) ~isempty(strfind(x,'post')),G),cellfun(@(x) ~isempty(strfind(x,'Post')),G)));
for q=1:length(cfold2)
    if (~contains(cfold2{q}, 'test') && ~contains(cfold2{q}, 'Test'))
%         cfold3=[cfold3; cfold2{q}];
        cfold3=strvcat(cfold3, cfold2{q});
    end
end
 cfold2=cellstr(cfold3)';

%%
%Ignore trial 6
for ind=1:length(cfold2)
  if  ~(contains(cfold2{ind},'trial1') ||contains(cfold2{ind},'trial2')||contains(cfold2{ind},'trial3')||contains(cfold2{ind},'trial4')||contains(cfold2{ind},'trial5')...
        ||contains(cfold2{ind},'Trial1')||contains(cfold2{ind},'Trial2')||contains(cfold2{ind},'Trial3')||contains(cfold2{ind},'Trial4')||contains(cfold2{ind},'Trial5')  )
      
      cfold2{ind}=[];    
  end
end

cfold2=cfold2(~cellfun('isempty',cfold2));

G=[cfold cfold2];

        
              
        if isempty(G) 
            no_folder=1;
            %g=NaN;
        else
            no_folder=0;
%xo
            for i=1:length(G); 
                clear states
                cd(G{i})

%xo
%Load HPC and PFC. 
%Get channels for current rat.

% vr=getfield(channels,strcat('Rat',num2str(Rat)));%Electrode channels. 

% HPC=load_open_ephys_data(['100_CH' num2str(vr(1)) '_0.continuous']);
% HPC=HPC.*(0.195);
% 
% Cortex=load_open_ephys_data(['100_CH' num2str(vr(2)) '_0.continuous']);
% Cortex=Cortex.*(0.195);
                                      

                    if and(~contains(G{i},'trial5'),~contains(G{i},'Trial5')) %Whenever it is not PostTrial 5 
                        
                                                     
    
                    elseif contains(G{i}, 'rial5') % PostTrial 5 case 
                                                                                        
                    end

%%

                    cd .. %Means there is no sleep scoring file.
           
            end
                cd ..
        end
        
%xo
       cd(g{j})
%    ripple_timestamps={};
   ripple_phases={};
   ripple_count =[];
   NREM_min = [];
   
               for i=1:length(G) % Trial Index
                   
                cd(G{i})
                clear states
                clear HPC Cortex
                %xo
                %if sum(contains(A, 'states')) > 0 %More than 2 sleep scoring files
%                     if sum(contains(A, 'states')) > 0
                    

vr=getfield(channels,strcat('Rat',num2str(Rat)));%Electrode channels. 

HPC=load_open_ephys_data(['100_CH' num2str(vr(1)) '_0.continuous']);
HPC=HPC.*(0.195);

Wn=[fs_new/fs ]; % Cutoff=fs_new/2 Hz. 
[b,a] = butter(3,Wn);
HPC=filtfilt(b,a,HPC);
HPC=downsample(HPC,fs/fs_new);

Cortex=load_open_ephys_data(['100_CH' num2str(vr(2)) '_0.continuous']);
Cortex=Cortex.*(0.195);

Cortex=filtfilt(b,a,Cortex);
Cortex=downsample(Cortex,fs/fs_new);

                                      

                    if and(~contains(G{i},'trial5'),~contains(G{i},'Trial5')) %Whenever it is not PostTrial 5 
                        
                                                    % Sleep Scoring data

                            % [swr_hpc,swr_pfc,s_hpc,s_pfc,V_hpc,V_pfc,signal2_hpc,signal2_pfc,sd_swr, M_multiplets, Mx_multiplets, multiplets, ripples, Mono_hpc, Mono_pfc,total_swrs,total_NREM_min ]=ripple_detection(HPC,Cortex,states,ss,offset1,offset2,TT,j,i);


                            %Load ripple timestamps.

                            ripple_timestamps=rip_timestamps{j}{i};
                            if ~iscell(ripple_timestamps) & isnan(ripple_timestamps)
                                warning([G{i} ' has no ripples'])
                                clear ripple_timestamps HPC Cortex
                                cd ..
                                continue
                            end



                            ripple_peak_timestamps=ripple_timestamps(:,3); % Extract only the ripple peaks.
                            ripple_peak_timestamps=[ripple_peak_timestamps{:}]; %Values in seconds.

                            ripple_end_timestamps=ripple_timestamps(:,2); % Extract only the ripple ends.
                            ripple_end_timestamps=[ripple_end_timestamps{:}]; %Values in seconds.

                            ripple_start_timestamps=ripple_timestamps(:,1); % Extract only the ripple starts.
                            ripple_start_timestamps=[ripple_start_timestamps{:}]; %Values in seconds.

                            %xo


                            %i is a trial index.
                            %j is the study day. 

                            %% Waveforms and GC Windows
                            % if iscell(Mono_hpc)
                            % concatenated_NREM_hpc = vertcat(Mono_hpc{:});
                            % concatenated_NREM_pfc = vertcat(Mono_pfc{:});
                            concatenated_NREM_hpc = HPC;
                            concatenated_NREM_pfc = Cortex;

                            waveforms_ripples={};
                            waveforms_ripples_umap=[];
                            GC_window_ripples = {};
                                for c=1:length(ripple_peak_timestamps)

                                    if ripple_peak_timestamps(c)*fs_new+1 < 3 * fs_new || ripple_peak_timestamps(c)*fs_new+1+(3*fs_new) > length(concatenated_NREM_hpc)
                                      continue     
                                   else
                                   GC_window_ripples{c,1} = [concatenated_NREM_pfc(int32(ripple_peak_timestamps(c)*fs_new+1-(3*fs_new)) : int32(ripple_peak_timestamps(c)*fs_new+1+(3*fs_new)))].';
                                   GC_window_ripples{c,1}(2,:) = concatenated_NREM_hpc(int32(ripple_peak_timestamps(c)*fs_new+1-(3*fs_new)) : int32(ripple_peak_timestamps(c)*fs_new+1+(3*fs_new)));

                                   waveforms_ripples{c,1}= concatenated_NREM_hpc(int32(ripple_start_timestamps(c)*fs_new+1):int32(ripple_end_timestamps(c)*fs_new+1));
                                   waveforms_ripples_umap(c,:)= concatenated_NREM_hpc(int32(ripple_peak_timestamps(c)*fs_new)-.025*fs_new:int32(ripple_peak_timestamps(c)*fs_new+1)+.025*fs_new);

                                   end
                                end

                     
                            % if iscell(V_hpc)
                            % % % %Broadband
                            % % % concatenated_NREM_hpc_broadband = vertcat(V_hpc{:});
                            % % % concatenated_NREM_pfc_broadband = vertcat(V_pfc{:});
                            % % % waveforms_ripples_broadband = {};
                            % % % GC_window_ripples_broadband = {};
                            % % %     for c=1:size(ripples,1)  
                            % % %        waveforms_ripples_broadband{c,1} = concatenated_NREM_hpc_broadband(int32(ripples(c,5)*1000+1):int32(ripples(c,7)*1000+1));
                            % % %        if ripples(c,6)*1000+1 < 1200 || ripples(c,6)*1000+1+(1.2*1000) > length(concatenated_NREM_hpc_broadband)
                            % % %           continue     
                            % % %        else
                            % % %        GC_window_ripples_broadband{c,1} = [concatenated_NREM_pfc_broadband(int32(ripples(c,6)*1000+1-(1.2*1000)) : int32(ripples(c,6)*1000+1+(1.2*1000)))].';
                            % % %        GC_window_ripples_broadband{c,1}(2,:) = concatenated_NREM_hpc_broadband(int32(ripples(c,6)*1000+1-(1.2*1000)) : int32(ripples(c,6)*1000+1+(1.2*1000)));
                            % % %        end
                            % % %     end
                            % else
                            %     waveforms_ripples_broadband = {NaN};
                            %     GC_window_ripples_broadband = {NaN};
                            % end

                            % if length(waveforms_ripples_broadband)~=1
                            %     for c =  1:length(waveforms_ripples_broadband)
                            %     temp_waveform =  waveforms_ripples_broadband{c};
                            %     GC_window_ripples{c,1} = [temp_waveform(int32(ripples(c,6)*1000+1) : int32(ripples(c,6)*1000+1+(1.2*1000)))];
                            %     end 
                            % end 

                            %xo
                            ripple_waveform_total{i} = waveforms_ripples;
                            % ripple_waveform_broadband_total{i} = waveforms_ripples_broadband;
                            GC_window_ripples_total{i} = GC_window_ripples;
                            % GC_window_ripples_broadband_total{i} = GC_window_ripples_broadband;
                            ripple_waveform_umap_total{i} = waveforms_ripples_umap;


                    end

                   if contains(G{i}, 'rial5')
                       if  length(G)~=6 
                           'Found more folders than expected, check if there are two PT5 folders.'
                           warning('Merging PT5 and PT5_2')
                           HPC_1=HPC;
                           Cortex_1=Cortex;
                           %xo
                           if length(HPC_1)>length(Cortex_1)
                               HPC_1=HPC_1(1:length(Cortex_1));
                           else
                               Cortex_1=Cortex_1(1:length(HPC_1));
                           end
                           cd ..
                           %xo
%                            i=i+1;
%                            cd(G{i})
%                            messbox(G{i},'Extra folder')
                           %i=i+1;
                           cd(G{i+1})
                           messbox(G{i+1},'Extra folder')                           
  
                           
                            HPC=load_open_ephys_data(['100_CH' num2str(vr(1)) '_0.continuous']);
                            HPC=HPC.*(0.195);

                            Wn=[fs_new/fs ]; % Cutoff=fs_new/2 Hz. 
                            [b,a] = butter(3,Wn);
                            HPC=filtfilt(b,a,HPC);
                            HPC=downsample(HPC,fs/fs_new);

                            Cortex=load_open_ephys_data(['100_CH' num2str(vr(2)) '_0.continuous']);
                            Cortex=Cortex.*(0.195);

                            Cortex=filtfilt(b,a,Cortex);
                            Cortex=downsample(Cortex,fs/fs_new);
                           
                           HPC_2=HPC;
                           Cortex_2=Cortex;
                           if length(HPC_2)>length(Cortex_2)
                               HPC_2=HPC_2(1:length(Cortex_2));
                           else
                               Cortex_2=Cortex_2(1:length(HPC_2));
                           end
                           
                           HPC=[HPC_1; HPC_2];
                           Cortex=[Cortex_1; Cortex_2];
                           
                           
                       end
                       clear HPC_1 HPC_2 HPC_3 HPC_4 Cortex_1 Cortex_2 Cortex_3 Cortex_4
                                                                                                                                %Sleep scoring data
  

                       %Ephys. Make length exactly 3 hours.
                        if length(HPC)<45*60*fs_new*4 % 4 times 45= 3 hours
                            HPC=[HPC.' (nan(45*60*fs_new*4-length(HPC),1).')]; %Fill with NaNs.
                        else
                            HPC=HPC(1:45*60*fs_new*4).'; %Take only 45 min.
                        end
                        
                        if length(Cortex)<45*60*fs_new*4
                            Cortex=[Cortex.' (nan(45*60*fs_new*4-length(Cortex),1).')]; %Fill with NaNs.
                        else
                            Cortex=Cortex(1:45*60*fs_new*4).'; %Take only 45 min.
                        end

                        
                           for jj = 1:4
                                   pfc = Cortex((2700*fs_new*(jj-1))+1:2700*fs_new*jj); 
                                   hpc = HPC((2700*fs_new*(jj-1))+1:2700*fs_new*jj);
                                   %states_chunk= states(2700*(jj-1)+1:2700*jj);
                                   %[swr_hpc, swr_pfc, s_hpc, s_pfc, V_hpc, V_pfc, signal2_hpc, signal2_pfc, sd_swr, M_multiplets, Mx_multiplets, multiplets, ripples, Mono_hpc, Mono_pfc,total_swrs,total_NREM_min]=ripple_detection(hpc,pfc,states_chunk,ss,offset1,offset2,TT,j,i); 

        %                            if iscell(Mono_hpc)
                                    concatenated_NREM_hpc = hpc;
                                    concatenated_NREM_pfc = pfc;
                                    waveforms_ripples = {};
                                    GC_window_ripples = {};
                                    waveforms_ripples_umap=[];
                                    
%%                                    % Load timestamps
                            ripple_timestamps=rip_timestamps{j}{5+jj};
                            if ~iscell(ripple_timestamps) & isnan(ripple_timestamps)
                                warning([G{i} '_' num2str(jj) ' has no ripples'])
                                clear ripple_timestamps HPC Cortex
                                cd ..
                                continue
                            end



                            ripple_peak_timestamps=ripple_timestamps(:,3); % Extract only the ripple peaks.
                            ripple_peak_timestamps=[ripple_peak_timestamps{:}]; %Values in seconds.

                            ripple_end_timestamps=ripple_timestamps(:,2); % Extract only the ripple ends.
                            ripple_end_timestamps=[ripple_end_timestamps{:}]; %Values in seconds.

                            ripple_start_timestamps=ripple_timestamps(:,1); % Extract only the ripple starts.
                            ripple_start_timestamps=[ripple_start_timestamps{:}]; %Values in seconds.
% xo
%                                      if jj==4 && length(G)>6
%                                          xo
%                                      end
%%                                    
                            waveforms_ripples={};
                            waveforms_ripples_umap=[];
                            GC_window_ripples = {};
                                        for c=1:length(ripple_peak_timestamps)
                                           if ripple_peak_timestamps(c)*fs_new+1 < 3 * fs_new || ripple_peak_timestamps(c)*fs_new+1+(3*fs_new) > length(concatenated_NREM_hpc)
                                              continue     
                                           else
                                               
%                                                GC_window_ripples{c,1} = [concatenated_NREM_pfc(int32(ripples(c,6)*1000+1-(1.2*1000)) : int32(ripples(c,6)*1000+1+(1.2*1000)))].';
%                                                GC_window_ripples{c,1}(2,:) = concatenated_NREM_hpc(int32(ripples(c,6)*1000+1-(1.2*1000)) : int32(ripples(c,6)*1000+1+(1.2*1000)));
                                                 GC_window_ripples{c,1} = [concatenated_NREM_pfc(int32(ripple_peak_timestamps(c)*fs_new+1-(3*fs_new)) : int32(ripple_peak_timestamps(c)*fs_new+1+(3*fs_new)))];
                                                 GC_window_ripples{c,1}(2,:) = concatenated_NREM_hpc(int32(ripple_peak_timestamps(c)*fs_new+1-(3*fs_new)) : int32(ripple_peak_timestamps(c)*fs_new+1+(3*fs_new)));                                            
%                                                  waveforms_ripples{c,1} = concatenated_NREM_hpc(int32(ripples(c,5)*1000+1):int32(ripples(c,7)*1000+1));                                           
                                                 waveforms_ripples{c,1}= concatenated_NREM_hpc(int32(ripple_start_timestamps(c)*fs_new+1):int32(ripple_end_timestamps(c)*fs_new+1));
                                                 waveforms_ripples_umap(c,:)= concatenated_NREM_hpc(int32(ripple_peak_timestamps(c)*fs_new)-.025*fs_new:int32(ripple_peak_timestamps(c)*fs_new+1)+.025*fs_new);

                                           
                                           end
                                        end
                                        %xo
%                                     else
%                                         waveforms_ripples = {NaN};
%                                         GC_window_ripples = {NaN};
        %                            end 

% % % %                                     if iscell(V_pfc)
% % % %                                     concatenated_NREM_hpc_broadband = vertcat(V_hpc{:});
% % % %                                     concatenated_NREM_pfc_broadband = vertcat(V_pfc{:});
% % % %                                     waveforms_ripples_broadband = {};
% % % %                                     GC_window_ripples_broadband = {};
% % % % 
% % % %                                         for c=1:size(ripples,1)
% % % % 
% % % %                                            waveforms_ripples_broadband{c,1}= concatenated_NREM_hpc_broadband(int32(ripples(c,5)*1000+1):int32(ripples(c,7)*1000+1));
% % % %         %                                    GC_window_ripples{c,1} = [concatenated_NREM_hpc_broadband(int32(ripples(c,6)*1000+1-(1.2*1000)) : int32(ripples(c,6)*1000));concatenated_NREM_hpc_broadband(int32(ripples(c,6)*1000+1) : int32(ripples(c,6)*1000+1+(1.2*1000)))];
% % % %         %                                    GC_window_ripples{c,1}(:,2) = [concatenated_NREM_pfc_broadband(int32(ripples(c,6)*1000+1-(1.2*1000)) : int32(ripples(c,6)*1000));concatenated_NREM_pfc_broadband(int32(ripples(c,6)*1000+1) : int32(ripples(c,6)*1000+1+(1.2*1000)))];
% % % %                                            if ripples(c,6)*1000+1 < 1200 || ripples(c,6)*1000+1+(1.2*1000) > length(concatenated_NREM_hpc_broadband)
% % % %                                               continue     
% % % %                                            else
% % % %                                                GC_window_ripples_broadband{c,1} = [concatenated_NREM_pfc_broadband(int32(ripples(c,6)*1000+1-(1.2*1000)) : int32(ripples(c,6)*1000+1+(1.2*1000)))].';
% % % %                                                GC_window_ripples_broadband{c,1}(2,:) = concatenated_NREM_hpc_broadband(int32(ripples(c,6)*1000+1-(1.2*1000)) : int32(ripples(c,6)*1000+1+(1.2*1000)));
% % % %                                            end 
% % % %                                         end
% % % %                                     else
% % % %                                         waveforms_ripples_broadband = {NaN};
% % % %                                         GC_window_ripples_broadband = {NaN};
% % % %                                     end 

                                  ripple_waveform_total{i+jj-1} = waveforms_ripples;
%                                   ripple_waveform_broadband_total{i+jj-1} = waveforms_ripples_broadband;                         
                                  GC_window_ripples_total{i+jj-1} = GC_window_ripples;
%                                   GC_window_ripples_broadband_total{i+jj-1} = GC_window_ripples_broadband;
                             ripple_waveform_umap_total{i+jj-1} = waveforms_ripples_umap;                                                

                           end    
                          
                   end
%                    end
                    
                %end
                        
                cd ..
% for r = 1:length(ripple_timestamps)
% if isnumeric(ripple_timestamps{r})
% ripple_timestamps{r} = NaN;
% ripple_phases{r} = NaN;
% end
% end 
if length(G)~=6 & contains(G{i}, 'rial5')

    break
end
               end
               %xo
                cd ..

% ripple_phases_comp = [ripple_phases_comp;ripple_phases];
ripple_waveform_comp = [ripple_waveform_comp; ripple_waveform_total];
% ripple_waveform_broadband_comp = [ripple_waveform_broadband_comp; ripple_waveform_broadband_total];
GC_window_ripples_comp = [GC_window_ripples_comp; GC_window_ripples_total];
% GC_window_ripples_broadband_comp = [GC_window_ripples_broadband_comp; GC_window_ripples_broadband_total];
ripple_waveform_umap_comp=[ripple_waveform_umap_comp; ripple_waveform_umap_total];
% 
% save(strcat('ripple_timestamps_',g{j},'.mat'),'ripple_timestamps')
% save(strcat('ripple_total_data_',g{j},'.mat'),'ripple_total_data')
% save(strcat('ripple_counts_',g{j},'.mat'),'ripple_count','NREM_min')
%xo
current_dir=cd;
cd('/home/adrian/Documents/UMAP/UMAP_RGS14')
save(strcat('ripple_waveforms_',g{j},'.mat'),'ripple_waveform_total')
% save(strcat('ripple_waveforms_broadband_',g{j},'.mat'),'ripple_waveform_broadband_total')
save(strcat('GC_window_ripples_',g{j},'.mat'),'GC_window_ripples_total')
% save(strcat('GC_window_ripples_broadband_',g{j},'.mat'),'GC_window_ripples_broadband_total')
save(strcat('ripple_waveforms_umap_',g{j},'.mat'),'ripple_waveform_umap_total')

save(strcat('ripple_waveforms_compilation_Rat',num2str(Rat),'.mat'),'ripple_waveform_comp')
% save(strcat('ripple_waveforms_broadband_compilation_Rat',rat_folder{k},'.mat'),'ripple_waveform_broadband_comp')
save(strcat('GC_window_ripples_compilation_Rat',num2str(Rat),'.mat'),'GC_window_ripples_comp','-v7.3')
% save(strcat('GC_window_ripples_broadband_compilation_Rat',rat_folder{k},'.mat'),'GC_window_ripples_broadband_comp')
save(strcat('ripple_waveforms_umap_compilation_Rat',num2str(Rat),'.mat'),'ripple_waveform_umap_comp')
cd(current_dir)
% save(strcat('ripple_phases_',g{j},'.mat'),'ripple_phases')
% save(strcat('ripple_phases_compilation_Rat',rat_folder{k},'.mat'),'ripple_phases_comp')

    end

    cd ..
        
