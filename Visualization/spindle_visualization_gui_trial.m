function varargout = spindle_visualization_gui_trial(varargin)
% SPINDLE_VISUALIZATION_GUI_TRIAL MATLAB code for spindle_visualization_gui_trial.fig
%      SPINDLE_VISUALIZATION_GUI_TRIAL, by itself, creates a new SPINDLE_VISUALIZATION_GUI_TRIAL or raises the existing
%      singleton*.
%
%      H = SPINDLE_VISUALIZATION_GUI_TRIAL returns the handle to a new SPINDLE_VISUALIZATION_GUI_TRIAL or the handle to
%      the existing singleton*.
%
%      SPINDLE_VISUALIZATION_GUI_TRIAL('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in SPINDLE_VISUALIZATION_GUI_TRIAL.M with the given input arguments.
%
%      SPINDLE_VISUALIZATION_GUI_TRIAL('Property','Value',...) creates a new SPINDLE_VISUALIZATION_GUI_TRIAL or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before spindle_visualization_gui_trial_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to spindle_visualization_gui_trial_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help spindle_visualization_gui_trial

% Last Modified by GUIDE v2.5 27-Jul-2022 13:28:57

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @spindle_visualization_gui_trial_OpeningFcn, ...
                   'gui_OutputFcn',  @spindle_visualization_gui_trial_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before spindle_visualization_gui_trial is made visible.
function spindle_visualization_gui_trial_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to spindle_visualization_gui_trial (see VARARGIN)

% Choose default command line output for spindle_visualization_gui_trial
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes spindle_visualization_gui_trial wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = spindle_visualization_gui_trial_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in pushbutton2.
function pushbutton2_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global val; global m; global spindles_waveform_broadband_total_visualization; global TotalSpindleChunks;
global SpindleSignal; global peaks; global Hippocamp; global Hippocamp_filtered; 
global SpindleFiltered; global spindles_bout_specific_timestamps;

addpath(genpath('/home/genzel/Documents/UMAP_Basic_OS/'))
[FileName,path]=uigetfile('*.*','.mat','MultiSelect','on');
waveform=FileName(find(contains(FileName,'waveforms')));
timestamps=FileName(find(contains(FileName,'timestamps')));
File=fullfile(path,waveform{1,1});
File2=fullfile(path,timestamps{1,1});
spindles_waveform_broadband_total_visualization=load(File);
spindles_waveform_broadband_total_visualization=spindles_waveform_broadband_total_visualization.spindles_waveform_broadband_total_visualization;
spindles_bout_specific_timestamps=load(File2);
spindles_bout_specific_timestamps=spindles_bout_specific_timestamps.spindles_bout_specific_timestamps;

prompt = {'Select a trial 1(presleep)-2(PT1)-3(PT2)-4(PT3)-5(PT4)-6(PT5.1)-7(PT5.2)-8(PT5.3)-9(PT5.4))'};
dlgtitle = 'Choose between (1-9)';
definput = {'9'};
ChosenPTforRD = inputdlg(prompt,dlgtitle,[1 80],definput); %Chosen PT for Ripple Detection
m=str2double(ChosenPTforRD{1, 1});

TotalSpindleChunks=length(spindles_waveform_broadband_total_visualization{1, m});  %find detection num
set(handles.text5,'string',TotalSpindleChunks);

msgbox("---- Spindles Succesfully Loaded ---- ");

% --- Executes on slider movement.
function slider2_Callback(hObject, eventdata, handles)
% hObject    handle to slider2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global val; global m; global spindles_waveform_broadband_total_visualization; global TotalSpindleChunks;
global SpindleSignal; global peakss; global Hippocamp; global Hippocamp_filtered; 
global SpindleFiltered; global spindles_bout_specific_timestamps; global starts;
global finishes; global peaklineLoc; global startlineLoc; global endlineLoc;

fn=2500;

val=get(handles.slider2,'Value');
val=round(val);
set(handles.text4,'string',val);

% set(handles.slider1, 'Min', 2);
set(handles.slider2, 'Max', TotalSpindleChunks);
set(handles.slider2, 'SliderStep', [1/(TotalSpindleChunks-2) , 10/(TotalSpindleChunks-2) ]);

SpindleSignal=spindles_waveform_broadband_total_visualization{1, m}{val, 1}; 
Wn1 = [9/(fn/2) 20/(fn/2)]; % 9-20Hz
[b2,a2] = butter(3,Wn1,'bandpass'); %Filter coefficients
SpindleFiltered=filtfilt(b2,a2,spindles_waveform_broadband_total_visualization{1, m}{val, 1});
peakss=[];
for i=1:length(spindles_bout_specific_timestamps{1, m});
    peakss=[peakss spindles_bout_specific_timestamps{1, m}{i, 3}];
end
peakss=peakss*2500;

starts=[];
for i=1:length(spindles_bout_specific_timestamps{1, m});
    starts=[starts spindles_bout_specific_timestamps{1, m}{i, 1}];
end
starts=starts*2500;
% 
finishes=[];
for i=1:length(spindles_bout_specific_timestamps{1, m});
    finishes=[finishes spindles_bout_specific_timestamps{1, m}{i, 2}];
end
finishes=finishes*2500;

% searching=spindles_waveform_broadband_total_visualization{1, m}{val, 1};
% ortalama=round(length(spindles_waveform_broadband_total_visualization{1, m}{val, 1}  )/2);
% basla=ortalama-round(length(spindles_waveform_broadband_total_visualization{1, m}{val, 1} ))/6;
% bitis=ortalama+round(length(spindles_waveform_broadband_total_visualization{1, m}{val, 1} ))/6;
% peak=max(searching(basla:bitis));
% peakpoint=find(searching==peak);
peakpoint=7500+(peakss(val)-starts(val));
startlineLoc=peakpoint-(peakss(val)-starts(val));
peaklineLoc= peakpoint;
endlineLoc=peakpoint+(finishes(val)-peakss(val));

axes(handles.axes2);
cla;

plot(SpindleFiltered*2.5+1.5*abs(max(SpindleSignal)-min(SpindleFiltered)),'k')
text(length(SpindleFiltered),mean(SpindleFiltered*2.5+1.5*abs(max(SpindleSignal)-min(SpindleFiltered))),'\leftarrow Filtered')
hold on
plot(SpindleSignal,'b')
text(length(SpindleSignal),mean(SpindleSignal),'\leftarrow Raw')

set(gca,'XTick',0:1000:length(SpindleSignal));
set(gca,'XTickLabel',0:0.4:length(SpindleSignal)/2500);

xline(startlineLoc,'--');
xl=xline(peaklineLoc,'--', peakss(val)/2500);
xl.LabelVerticalAlignment = 'middle';
xl.LabelHorizontalAlignment = 'center';
xl.LabelOrientation = 'horizontal';
xline(endlineLoc,'--');

xlim tight
hold off

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider


% --- Executes during object creation, after setting all properties.
function slider2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to slider2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end
