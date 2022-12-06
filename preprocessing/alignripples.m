function [Y]=alignripples(x)
% Align ripples to the closest minimum nearest to the ripple peak.
if size(x,2)> 1 % In case we stored more data besides the waveforms. This is the case in OS and more recently preprocessed datasets. 
    x=x(:,1);
end
% Input
% x is the cell array obtained from the GC files. Each cell is one ripple. 
Fs=2500;
Wn1=[100/(Fs/2) 300/(Fs/2)]; % Cutoff=100-300 Hz
[b,a] = butter(3,Wn1,'bandpass');
x=cell2mat(x);

x=x(2:2:end,:);
ripples=filtfilt(b,a,x.');
ripples=ripples.';
x=ripples;
%%

xPeak=7500+1; %Ripple Peak
% ripples=x;
Data=[];
coil = Fs * 0.010; %Original script used 0.010
Y=[];
for i=1:size(ripples,1)


                [ ~, minRaw] = min( ripples(i, (xPeak-coil):(xPeak+coil)) );
                minRaw = xPeak-coil + minRaw-1;
%                 Data=[Data minRaw];
%                 y=x(i, minRaw-3*Fs+coil : minRaw+3*Fs-coil );
                y=x(i, minRaw-126/2 : minRaw+126/2 );

                Y=[Y; y];
end
end