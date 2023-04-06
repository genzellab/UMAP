function [rip_duration, rip_phase, SO_b, SO_a, rip_threshold]=extra_features(x)
% Extract extra features
addpath(genpath('/home/adrian/Downloads/chronux_2_12.v03/chronux_2_12'))

%x=GC_window_ripples_broadband_total{1};
if size(x,2)> 1 % In case we stored more data besides the waveforms. This is the case in OS and more recently preprocessed datasets. 
    %x=x(:,1);
    
    rip_duration=cell2mat(x(:,5))*1000; %Duration in milliseconds
    rip_phase=cell2mat(x(:,6));
    try
        rip_threshold=cell2mat(x(:,7));
    catch
        rip_threshold=cell2mat(x(:,6))*0;  %multiplied by zero for now
    end
    % Cortical features
    x=x(:,1);
    x=cell2mat(x);
    x=x(1:2:end,:);
%%
SO_b=[];
SO_a=[];

parfor ii=1:size(x,1)
    y=x(ii,:);
    [so_b,so_a]=so_mean_power(y);

SO_b=[SO_b so_b];
SO_a=[SO_a so_a];
    
end

SO_b=SO_b';
SO_a=SO_a';

%%

% %%
% histogram(SO_b,[0:1000 :20000],'FaceColor','r')
% hold on
% histogram(SO_a,[0:1000 :20000],'FaceColor','b')
% alpha(0.2)

%%
    
else
%    error('Data missing')
rip_duration=[];
rip_phase=[];
SO_b=[];
SO_a=[];
rip_threshold=[];

end
end