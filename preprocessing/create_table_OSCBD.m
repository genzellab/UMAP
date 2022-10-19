% Organize data in a table format
%% vehicle

Treatment=fieldnames(CBD);
Rats=CBD.(Treatment{1});
Rats=fieldnames(Rats);
StudyDays=fieldnames(CBD.(Treatment{1}).(Rats{1}));
TrialNames={'Presleep','Post1','Post2','Post3','Post4','Post5-1','Post5-2','Post5-3','Post5-4'};
veh=[];
Treatment={'VEH','RGS14'};
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

Rats=fieldnames(RGS);
StudyDays=fieldnames(RGS.(Rats{1}));
TrialNames={'Presleep','Post1','Post2','Post3','Post4','Post5-1','Post5-2','Post5-3','Post5-4'};
rgs=[];
Treatment={'VEH','RGS14'};

for i=1:length(Rats)
    for j=1:length(StudyDays)
      Trials=RGS.(Rats{i}).(StudyDays{j});
      Rat=(Rats{i});
      StudyDay=StudyDays{j};
        for k=1:length(Trials)
            
            t=table(Treatment(2),{Rat},{StudyDay},{TrialNames{k}},Trials(k));
            rgs=[rgs;t];
        end
      
    end
end

 rgs.Properties.VariableNames=[ {'Treatment'} {'Rat'} {'StudyDay'} {'Trial'} {'Ripples'}];
 %%
 T=[veh;rgs];
 %% Compute/add features
 
 %% Amplitude
 ripple_amp=cellfun(@(x) max(abs(hilbert(x.'))) ,T.Ripples,'UniformOutput',false);

 T=[T ripple_amp];
 T.Properties.VariableNames(6)={'Amplitude'};
 
 %% Mean Freq
[ripple_meanfreq]=cellfun(@(x) (compute_meanfreq(x)) ,T.Ripples,'UniformOutput',false);

 T=[T ripple_meanfreq];
 T.Properties.VariableNames(7)={'Mean frequency'};
  