clearvars
t = readtable('sequences_cooccurences_basic_NSD.xlsx');
basic_i = contains(table2cell(t(:,1)),'BASIC');
nsd_i = contains(table2cell(t(:,1)),'NSD');
condition  = table2cell(t(:,4));
condition_basic = condition(basic_i);
condition_nsd = condition(nsd_i);
trial = table2cell(t(:,5));
trial_basic = trial(basic_i);
trial_nsd = trial(nsd_i);
DSwR = table2cell(t(:,19));
DSwR_basic = DSwR(basic_i);
DSwR_nsd = DSwR(nsd_i);

hc_basic{1,1} = cell2mat(DSwR_basic(contains(condition_basic,'HC') & contains(trial_basic,'PS')));
hc_basic{1,2} = cell2mat(DSwR_basic(contains(condition_basic,'HC') & contains(trial_basic,'PT1'))) ;
hc_basic{1,3} = cell2mat(DSwR_basic(contains(condition_basic,'HC') & contains(trial_basic,'PT2')));
hc_basic{1,4} = cell2mat(DSwR_basic(contains(condition_basic,'HC') & contains(trial_basic,'PT3')));
hc_basic{1,5} = cell2mat(DSwR_basic(contains(condition_basic,'HC') & contains(trial_basic,'PT4')));
hc_basic{1,6} = cell2mat(DSwR_basic(contains(condition_basic,'HC') & contains(trial_basic,'PT5_1'))) ;
hc_basic{1,7} = cell2mat(DSwR_basic(contains(condition_basic,'HC') & contains(trial_basic,'PT5_2'))) ;
hc_basic{1,8} = cell2mat(DSwR_basic(contains(condition_basic,'HC') & contains(trial_basic,'PT5_3'))) ;
hc_basic{1,9} = cell2mat(DSwR_basic(contains(condition_basic,'HC') & contains(trial_basic,'PT5_4'))) ;

or_basic{1,1} = cell2mat(DSwR_basic(contains(condition_basic,'OR') & contains(trial_basic,'PS')));
or_basic{1,2} = cell2mat(DSwR_basic(contains(condition_basic,'OR') & contains(trial_basic,'PT1'))) ;
or_basic{1,3} = cell2mat(DSwR_basic(contains(condition_basic,'OR') & contains(trial_basic,'PT2')));
or_basic{1,4} = cell2mat(DSwR_basic(contains(condition_basic,'OR') & contains(trial_basic,'PT3')));
or_basic{1,5} = cell2mat(DSwR_basic(contains(condition_basic,'OR') & contains(trial_basic,'PT4')));
or_basic{1,6} = cell2mat(DSwR_basic(contains(condition_basic,'OR') & contains(trial_basic,'PT5_1'))) ;
or_basic{1,7} = cell2mat(DSwR_basic(contains(condition_basic,'OR') & contains(trial_basic,'PT5_2'))) ;
or_basic{1,8} = cell2mat(DSwR_basic(contains(condition_basic,'OR') & contains(trial_basic,'PT5_3'))) ;
or_basic{1,9} = cell2mat(DSwR_basic(contains(condition_basic,'OR') & contains(trial_basic,'PT5_4'))) ;

con_basic{1,1} = cell2mat(DSwR_basic(contains(condition_basic,'CON') & contains(trial_basic,'PS')));
con_basic{1,2} = cell2mat(DSwR_basic(contains(condition_basic,'CON') & contains(trial_basic,'PT1')));
con_basic{1,3} = cell2mat(DSwR_basic(contains(condition_basic,'CON') & contains(trial_basic,'PT2')));
con_basic{1,4} = cell2mat(DSwR_basic(contains(condition_basic,'CON') & contains(trial_basic,'PT3')));
con_basic{1,5} = cell2mat(DSwR_basic(contains(condition_basic,'CON') & contains(trial_basic,'PT4')));
con_basic{1,6} = cell2mat(DSwR_basic(contains(condition_basic,'CON') & contains(trial_basic,'PT5_1'))) ;
con_basic{1,7} = cell2mat(DSwR_basic(contains(condition_basic,'CON') & contains(trial_basic,'PT5_2'))) ;
con_basic{1,8} = cell2mat(DSwR_basic(contains(condition_basic,'CON') & contains(trial_basic,'PT5_3'))) ;
con_basic{1,9} = cell2mat(DSwR_basic(contains(condition_basic,'CON') & contains(trial_basic,'PT5_4'))) ;

orn_basic{1,1} = cell2mat(DSwR_basic(contains(condition_basic,'OR_N') & contains(trial_basic,'PS')));
orn_basic{1,2} = cell2mat(DSwR_basic(contains(condition_basic,'OR_N') & contains(trial_basic,'PT1')));
orn_basic{1,3} = cell2mat(DSwR_basic(contains(condition_basic,'OR_N') & contains(trial_basic,'PT2')));
orn_basic{1,4} = cell2mat(DSwR_basic(contains(condition_basic,'OR_N') & contains(trial_basic,'PT3')));
orn_basic{1,5} = cell2mat(DSwR_basic(contains(condition_basic,'OR_N') & contains(trial_basic,'PT4')));
orn_basic{1,6} = cell2mat(DSwR_basic(contains(condition_basic,'OR_N') & contains(trial_basic,'PT5_1'))) ;
orn_basic{1,7} = cell2mat(DSwR_basic(contains(condition_basic,'OR_N') & contains(trial_basic,'PT5_2'))) ;
orn_basic{1,8} = cell2mat(DSwR_basic(contains(condition_basic,'OR_N') & contains(trial_basic,'PT5_3'))) ;
orn_basic{1,9} = cell2mat(DSwR_basic(contains(condition_basic,'OR_N') & contains(trial_basic,'PT5_4'))) ;

od_basic{1,1} = cell2mat(DSwR_basic(contains(condition_basic,'OD') & contains(trial_basic,'PS')));
od_basic{1,2} = cell2mat(DSwR_basic(contains(condition_basic,'OD') & contains(trial_basic,'PT1')));
od_basic{1,3} = cell2mat(DSwR_basic(contains(condition_basic,'OD') & contains(trial_basic,'PT2')));
od_basic{1,4} = cell2mat(DSwR_basic(contains(condition_basic,'OD') & contains(trial_basic,'PT3')));
od_basic{1,5} = cell2mat(DSwR_basic(contains(condition_basic,'OD') & contains(trial_basic,'PT4')));
od_basic{1,6} = cell2mat(DSwR_basic(contains(condition_basic,'OD') & contains(trial_basic,'PT5_1'))) ;
od_basic{1,7} = cell2mat(DSwR_basic(contains(condition_basic,'OD') & contains(trial_basic,'PT5_2'))) ;
od_basic{1,8} = cell2mat(DSwR_basic(contains(condition_basic,'OD') & contains(trial_basic,'PT5_3'))) ;
od_basic{1,9} = cell2mat(DSwR_basic(contains(condition_basic,'OD') & contains(trial_basic,'PT5_4'))) ;

or_nsd{1,1} = cell2mat(DSwR_nsd(contains(condition_nsd,'OR') & contains(trial_nsd,'PS')));
or_nsd{1,2} = cell2mat(DSwR_nsd(contains(condition_nsd,'OR') & contains(trial_nsd,'PT1'))) ;
or_nsd{1,3} = cell2mat(DSwR_nsd(contains(condition_nsd,'OR') & contains(trial_nsd,'PT2')));
or_nsd{1,4} = cell2mat(DSwR_nsd(contains(condition_nsd,'OR') & contains(trial_nsd,'PT3')));
or_nsd{1,5} = cell2mat(DSwR_nsd(contains(condition_nsd,'OR') & contains(trial_nsd,'PT4')));
or_nsd{1,6} = cell2mat(DSwR_nsd(contains(condition_nsd,'OR') & contains(trial_nsd,'PT5_1'))) ;
or_nsd{1,7} = cell2mat(DSwR_nsd(contains(condition_nsd,'OR') & contains(trial_nsd,'PT5_2'))) ;
or_nsd{1,8} = cell2mat(DSwR_nsd(contains(condition_nsd,'OR') & contains(trial_nsd,'PT5_3'))) ;
or_nsd{1,9} = cell2mat(DSwR_nsd(contains(condition_nsd,'OR') & contains(trial_nsd,'PT5_4'))) ;

orn_nsd{1,1} = cell2mat(DSwR_nsd(contains(condition_nsd,'OR_N') & contains(trial_nsd,'PS')));
orn_nsd{1,2} = cell2mat(DSwR_nsd(contains(condition_nsd,'OR_N') & contains(trial_nsd,'PT1')));
orn_nsd{1,3} = cell2mat(DSwR_nsd(contains(condition_nsd,'OR_N') & contains(trial_nsd,'PT2')));
orn_nsd{1,4} = cell2mat(DSwR_nsd(contains(condition_nsd,'OR_N') & contains(trial_nsd,'PT3')));
orn_nsd{1,5} = cell2mat(DSwR_nsd(contains(condition_nsd,'OR_N') & contains(trial_nsd,'PT4')));
orn_nsd{1,6} = cell2mat(DSwR_nsd(contains(condition_nsd,'OR_N') & contains(trial_nsd,'PT5_1'))) ;
orn_nsd{1,7} = cell2mat(DSwR_nsd(contains(condition_nsd,'OR_N') & contains(trial_nsd,'PT5_2'))) ;
orn_nsd{1,8} = cell2mat(DSwR_nsd(contains(condition_nsd,'OR_N') & contains(trial_nsd,'PT5_3'))) ;
orn_nsd{1,9} = cell2mat(DSwR_nsd(contains(condition_nsd,'OR_N') & contains(trial_nsd,'PT5_4'))) ;

hc_basic = cell2mat(hc_basic);
od_basic = cell2mat(od_basic);
or_basic = cell2mat(or_basic);
con_basic = cell2mat(con_basic);
orn_basic = cell2mat(orn_basic);

or_nsd = cell2mat(or_nsd);
orn_nsd = cell2mat(orn_nsd);

or_orn_nsd = [or_basic;or_nsd];
orn_or_nsd = [orn_basic;or_nsd];

mean_hc_basic = mean(hc_basic,1);
mean_od_basic = mean(od_basic,1);
mean_or_basic = mean(or_basic,1);
mean_orn_basic = mean(orn_basic,1);
mean_con_basic = mean(con_basic,1);

mean_or_nsd = mean(or_nsd,1);
mean_orn_nsd = mean(orn_nsd,1);

mean_or_orn_nsd = mean (or_orn_nsd,1);
mean_orn_or_nsd =  mean(orn_or_nsd,1);

sem_hc_basic = std(hc_basic,1)./sqrt(size(hc_basic,1));
sem_od_basic = std(od_basic,1)./sqrt(size(od_basic,1));
sem_or_basic = std(or_basic,1)./sqrt(size(or_basic,1));
sem_con_basic = std(con_basic,1)./sqrt(size(con_basic,1));
sem_orn_basic = std(orn_basic,1)./sqrt(size(orn_basic,1));

sem_or_nsd = std(or_nsd,1)./sqrt(size(or_nsd,1));
sem_orn_nsd = std(orn_nsd,1)./sqrt(size(orn_nsd,1));

sem_or_orn_nsd = std(or_orn_nsd,1)./sqrt(size(or_orn_nsd,1));
sem_orn_or_nsd = std(orn_or_nsd,1)./sqrt(size(orn_or_nsd,1));


figure
hold on
plot([1:9], mean_hc_basic, '-o', 'LineWidth', 2 , 'color','#0072BD')
scatter([1:9],mean_hc_basic,80,'filled','MarkerFaceColor','#0072BD')
errorbar([1:9],mean_hc_basic,sem_hc_basic,'Color', [0.502 0.502 0.502] ,'LineWidth',1)

plot([1:9], mean_od_basic, '-o', 'LineWidth', 2 ,'color','#77AC30')
scatter([1:9],mean_od_basic,80,'filled','MarkerFaceColor','#77AC30')
errorbar([1:9],mean_od_basic,sem_od_basic,'Color', [0.502 0.502 0.502] ,'LineWidth',1)

plot([1:9], mean_con_basic, '-o', 'LineWidth', 2 ,'color','#D95319')
scatter([1:9],mean_con_basic,80,'filled','MarkerFaceColor','#D95319')
errorbar([1:9],mean_con_basic,sem_con_basic,'Color', [0.502 0.502 0.502] ,'LineWidth',1)

plot([1:9], mean_or_basic, '-o', 'LineWidth', 2 ,'color','#FF0000')
scatter([1:9],mean_or_basic,80,'filled','MarkerFaceColor','#FF0000')
errorbar([1:9],mean_or_basic,sem_or_basic,'Color', [0.502 0.502 0.502] ,'LineWidth',1)

plot([1:9], mean_orn_nsd, '-o', 'LineWidth', 2,'color','#5E2C04')
scatter([1:9],mean_orn_nsd,80,'filled','MarkerFaceColor','#5E2C04')
errorbar([1:9],mean_orn_nsd,sem_orn_nsd,'Color', [0.502 0.502 0.502] ,'LineWidth',1)

plot([1:9], mean_or_orn_nsd, '-o', 'LineWidth', 2 ,'color','#B200ED')
scatter([1:9],mean_or_orn_nsd,80,'filled','MarkerFaceColor','#B200ED')
errorbar([1:9],mean_or_orn_nsd,sem_or_orn_nsd,'Color', [0.502 0.502 0.502] ,'LineWidth',1)

plot([1:9], mean_orn_basic, '-o', 'LineWidth', 2 ,'color','#FC74FD')
scatter([1:9],mean_orn_basic,80,'filled','MarkerFaceColor','#FC74FD')
errorbar([1:9],mean_orn_basic,sem_orn_basic,'Color', [0.502 0.502 0.502] ,'LineWidth',1)

plot([1:9], mean_or_nsd, '-o', 'LineWidth', 2 ,'color','#173518')
scatter([1:9],mean_or_nsd,80,'filled','MarkerFaceColor','#173518')
errorbar([1:9],mean_or_nsd,sem_or_nsd,'Color', [0.502 0.502 0.502] ,'LineWidth',1)

plot([1:9],mean_orn_or_nsd, '-o', 'LineWidth', 2 ,'color','#808080')
scatter([1:9],mean_orn_or_nsd,80,'filled','MarkerFaceColor','#808080')
errorbar([1:9],mean_orn_or_nsd,sem_orn_or_nsd,'Color', [0.502 0.502 0.502] ,'LineWidth',1)

xlim([0.5 9.5])
ax=gca;
ax.XTickLabel=[{'PS'};{'PT1'};{'PT2'};{'PT3'};{'PT4'};{'PT5_1'};{'PT5_2'};{'PT5_3'};{'PT5_4'}];
ylabel('Average count')
% legend('HC','HC','HC','OD','OD','OD','CON','CON','CON','OR','OR','OR','OR_NN_S','OR_NN_S','OR_NN_S','OR+OR_NN_S','OR+OR_NN_S','OR+OR_NN_S','OR_N','OR_N','OR_N','OR_N_S','OR_N_S','OR_N_S','OR_N+OR_N_S','OR_N+OR_N_S','OR_N+OR_N_S')
legend('','HC','','','OD','','','CON','','','OR','','','OR__NN__S','','','OR+OR__NN__S','','','OR__N','','','OR__N__S','','','OR__N+OR__N__S','')

title('Average DSwR counts')

Counts_wo_OD_CON
