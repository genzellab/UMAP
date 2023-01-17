% Organize data in a table format
%% vehicle

Treatment=fieldnames(CBD);
Rats=CBD.(Treatment{1});
Rats=fieldnames(Rats);
StudyDays=fieldnames(CBD.(Treatment{1}).(Rats{1}));
TrialNames={'Presleep','Post1','Post2','Post3','Post4','Post5-1','Post5-2','Post5-3','Post5-4'};
veh=[];
Treatment={'VEH','CBD'};
Dataset='CBDchronic';
%%
for l=1:length(Treatment)
    for i=1:length(Rats)
        for j=1:length(StudyDays)
            %xo
          Trials=CBD.(Treatment{l}).(Rats{i}).(StudyDays{j});
          Rat=(Rats{i});
          StudyDay=StudyDays{j};
            for k=1:length(Trials)
                %xo
                t=table({Dataset},Treatment(l),{Rat},{StudyDay},{TrialNames{k}},Trials(k));
                veh=[veh;t];
            end

        end
    end
end

%%
 veh.Properties.VariableNames=[{'Dataset'} {'Treatment'} {'Rat'} {'StudyDay'} {'Trial'} {'Ripples'}];
 xo
%% OS BASIC

Treatment=fieldnames(CBD);
Rats=CBD.(Treatment{1});
Rats=fieldnames(Rats);
StudyDays=fieldnames(CBD.(Treatment{1}).(Rats{1}));
TrialNames={'Presleep','Post1','Post2','Post3','Post4','Post5-1','Post5-2','Post5-3','Post5-4'};
veh=[];
%Treatment={'VEH','RGS14'};
Dataset='OSBASIC';
%%
for l=1:length(Treatment)
    for i=1:length(Rats)
        for j=1:length(StudyDays)
            %xo
          Trials=CBD.(Treatment{l}).(Rats{i}).(StudyDays{j});
          Rat=(Rats{i});
          StudyDay=StudyDays{j};
            for k=1:length(Trials)
                %xo
                t=table({Dataset},Treatment(l),{Rat},{StudyDay},{TrialNames{k}},Trials(k));
                veh=[veh;t];
            end

        end
    end
end

%%
 veh.Properties.VariableNames=[{'Dataset'} {'Treatment'} {'Rat'} {'StudyDay'} {'Trial'} {'Ripples'}];

%% RGS14

Treatment=fieldnames(CBD);
Treatment=Treatment(1);
Rats=CBD.(Treatment{1});
Rats=fieldnames(Rats);
StudyDays=fieldnames(CBD.(Treatment{1}).(Rats{1}));
TrialNames={'Presleep','Post1','Post2','Post3','Post4','Post5-1','Post5-2','Post5-3','Post5-4'};
veh=[];
%Rats=[Rats; fieldnames(CBD.(Treatment{2}))];
%Treatment={'VEH','RGS14'};
Dataset='RGS14';
%%
for l=1:length(Treatment)
    for i=1:length(Rats)
        for j=1:length(StudyDays)
            %xo
          Trials=CBD.(Treatment{l}).(Rats{i}).(StudyDays{j});
          Rat=(Rats{i});
          StudyDay=StudyDays{j};
            for k=1:length(Trials)
                %xo
                t=table({Dataset},Treatment(l),{Rat},{StudyDay},{TrialNames{k}},Trials(k));
                veh=[veh;t];
            end

        end
    end
end

%%
 veh.Properties.VariableNames=[{'Dataset'} {'Treatment'} {'Rat'} {'StudyDay'} {'Trial'} {'Ripples'}];


 
 
 
%% rgs14
Treatment=fieldnames(CBD);
Treatment=Treatment(2);
Rats=CBD.(Treatment{1});
Rats=fieldnames(Rats);
StudyDays=fieldnames(CBD.(Treatment{1}).(Rats{1}));
TrialNames={'Presleep','Post1','Post2','Post3','Post4','Post5-1','Post5-2','Post5-3','Post5-4'};
rgs=[];
%Rats=[Rats; fieldnames(CBD.(Treatment{2}))];
%Treatment={'rgs','RGS14'};
Dataset='RGS14';
%%
for l=1:length(Treatment)
    for i=1:length(Rats)
        for j=1:length(StudyDays)
            %xo
          Trials=CBD.(Treatment{l}).(Rats{i}).(StudyDays{j});
          Rat=(Rats{i});
          StudyDay=StudyDays{j};
            for k=1:length(Trials)
                %xo
                t=table({Dataset},Treatment(l),{Rat},{StudyDay},{TrialNames{k}},Trials(k));
                rgs=[rgs;t];
            end

        end
    end
end

%%
 rgs.Properties.VariableNames=[{'Dataset'} {'Treatment'} {'Rat'} {'StudyDay'} {'Trial'} {'Ripples'}];

 %rgs.Properties.VariableNames=[ {'Treatment'} {'Rat'} {'StudyDay'} {'Trial'} {'Ripples'}];
 %%
 T=[veh;rgs];
 %% Compute/add features
 
 %% Amplitude
 ripple_amp=cellfun(@(x) max(abs(hilbert(x.'))) ,T.Ripples,'UniformOutput',false);

 T=[T ripple_amp];
 T.Properties.VariableNames(7)={'Amplitude'};
 
 % Mean Freq
[ripple_meanfreq]=cellfun(@(x) (compute_meanfreq(x)) ,T.Ripples,'UniformOutput',false);

 T=[T ripple_meanfreq];
 T.Properties.VariableNames(8)={'Mean frequency'};
%% Spectral entropy
 %ripple_amp=cellfun(@(x) max(abs(hilbert(x.'))) ,T.Ripples,'UniformOutput',false);
 ripple_entropy=(cellfun(@(equis) spectral_entropy(equis,100,300,2500),T.Ripples,'UniformOutput',false  ));
 T=[T ripple_entropy];
 T.Properties.VariableNames(14)={'Spectral Entropy'};


%%
clearvars -except T
%%
% Organize FEATURE data in a table format
%% vehicle

Treatment=fieldnames(CBD);
Rats=CBD.(Treatment{1});
Rats=fieldnames(Rats);
StudyDays=fieldnames(CBD.(Treatment{1}).(Rats{1}));
TrialNames={'Presleep','Post1','Post2','Post3','Post4','Post5-1','Post5-2','Post5-3','Post5-4'};
veh=[];
Treatment={'VEH','CBD'};
Dataset='CBDchronic';
%%
for l=1:length(Treatment)
    for i=1:length(Rats)
        for j=1:length(StudyDays)
            %xo
          Trials=CBD.(Treatment{l}).(Rats{i}).(StudyDays{j});
          Trials=cellfun(@(x) x',Trials,'UniformOutput',false);
          
          Rat=(Rats{i});
          StudyDay=StudyDays{j};
            for k=1:length(Trials)
                %xo
                t=table({Dataset},Treatment(l),{Rat},{StudyDay},{TrialNames{k}},Trials(1,k),Trials(2,k),Trials(3,k),Trials(4,k),Trials(5,k));
                veh=[veh;t];
            end

        end
    end
end

%%
 veh.Properties.VariableNames=[{'Dataset'} {'Treatment'} {'Rat'} {'StudyDay'} {'Trial'} {'Duration'} {'Phase'} {'SO_power_before'} {'SO_power_after'} {'Threshold'}]; %rip_duration; rip_phase; SO_b; SO_a ;rip_threshold
 xo
 clearvars -except veh
T=[ T veh(:,6:end)]
 clearvars -except T

 
%% OS BASIC

Treatment=fieldnames(CBD);
Rats=CBD.(Treatment{1});
Rats=fieldnames(Rats);
StudyDays=fieldnames(CBD.(Treatment{1}).(Rats{1}));
TrialNames={'Presleep','Post1','Post2','Post3','Post4','Post5-1','Post5-2','Post5-3','Post5-4'};
veh=[];
%Treatment={'VEH','RGS14'};
Dataset='OSBASIC';
%%
for l=1:length(Treatment)
    for i=1:length(Rats)
        for j=1:length(StudyDays)
            %xo
          Trials=CBD.(Treatment{l}).(Rats{i}).(StudyDays{j});
          Trials=cellfun(@(x) x',Trials,'UniformOutput',false);

          Rat=(Rats{i});
          StudyDay=StudyDays{j};
            for k=1:length(Trials)
                %xo
                %t=table({Dataset},Treatment(l),{Rat},{StudyDay},{TrialNames{k}},Trials(k));
                t=table({Dataset},Treatment(l),{Rat},{StudyDay},{TrialNames{k}},Trials(1,k),Trials(2,k),Trials(3,k),Trials(4,k),Trials(5,k));
                veh=[veh;t];
            end

        end
    end
end

%%
% veh.Properties.VariableNames=[{'Dataset'} {'Treatment'} {'Rat'} {'StudyDay'} {'Trial'} {'Ripples'}];
 veh.Properties.VariableNames=[{'Dataset'} {'Treatment'} {'Rat'} {'StudyDay'} {'Trial'} {'Duration'} {'Phase'} {'SO_power_before'} {'SO_power_after'} {'Threshold'}]; %rip_duration; rip_phase; SO_b; SO_a ;rip_threshold
 xo
 clearvars -except veh
T=[ T veh(:,6:end)]
 clearvars -except T