figure
hold on
plot([1:9], mean_hc_basic, '-o', 'LineWidth', 2 , 'color','#0072BD')
scatter([1:9],mean_hc_basic,80,'filled','MarkerFaceColor','#0072BD')
errorbar([1:9],mean_hc_basic,sem_hc_basic,'Color', [0.502 0.502 0.502] ,'LineWidth',1)

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
ax = gca;
ax.XTickLabel = [{'PS'};{'PT1'};{'PT2'};{'PT3'};{'PT4'};{'PT5_1'};{'PT5_2'};{'PT5_3'};{'PT5_4'}];
ylabel('Average rates')
% legend('HC','HC','HC','OD','OD','OD','CON','CON','CON','OR','OR','OR','OR_NN_S','OR_NN_S','OR_NN_S','OR+OR_NN_S','OR+OR_NN_S','OR+OR_NN_S','OR_N','OR_N','OR_N','OR_N_S','OR_N_S','OR_N_S','OR_N+OR_N_S','OR_N+OR_N_S','OR_N+OR_N_S')
legend('','HC','','','OR','','','OR__NN__S','','','OR+OR__NN__S','','','OR__N','','','OR__N__S','','','OR__N+OR__N__S','')

title('Average DSwR rates w/o OD and CON')
