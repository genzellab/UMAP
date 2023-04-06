function [so_b,so_a]=so_mean_power(y)

    %% Compute power spectra
    leng=length(y);
    ro=7500;
    tm = create_timecell(ro,leng,2500);
    tm=tm(1);

    data.label=[{'PFC'}];
    data.time=tm;
    data.trial={y};


    % cfg1         = [];
    % cfg1.overlap = 0.25;
    % cfg1.length        = 6;
    %rpt     = ft_redefinetrial(cfg1, data);

    % periodogram
    cfg2 = [];
    cfg2.output  = 'pow';
    cfg2.channel = 'PFC';
    cfg2.method  = 'mtmconvol'; % multitaper
    cfg2.taper   = 'dpss';
    cfg2.keeptrials = 'yes';
    cfg2.foi     = 0:0.25:4; % 1/cfg1.length  = 4;
    %cfg2.foi     = 9:0.25:20; % 1/cfg1.length  = 4;

    cfg2.t_ftimwin = .1 * ones(size(cfg2.foi));
    cfg2.tapsmofrq = 10;
    cfg2.toi=tm{1}(find(tm{1}==-1):find(tm{1}==1));

    freq = ft_freqanalysis(cfg2, data);
    %% Plotting
%         cfg              = [];
%         cfg.channel      = freq.label{1};
%         [ zmin1, zmax1] = ft_getminmax(cfg, freq);
%         zlim=[zmin1 zmax1];
% 
%         cfg.zlim=zlim;
%         cfg.colormap=colormap(jet(256));
% 
%         ft_singleplotTFR(cfg, freq); 
%         xlabel('Time (s)')
%         ylabel('Frequency (Hz)')

    %%
    so=squeeze(freq.powspctrm);
    so_before=so(:,1:2501);
    so_after=so(:,2501:end);
    %%

    so_b=mean(so_before(:));
    so_a=mean(so_after(:));

end