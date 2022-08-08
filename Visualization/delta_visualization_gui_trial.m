function varargout = delta_visualization_gui_trial(varargin)
% DELTA_VISUALIZATION_GUI_TRIAL MATLAB code for delta_visualization_gui_trial.fig
%      DELTA_VISUALIZATION_GUI_TRIAL, by itself, creates a new DELTA_VISUALIZATION_GUI_TRIAL or raises the existing
%      singleton*.
%
%      H = DELTA_VISUALIZATION_GUI_TRIAL returns the handle to a new DELTA_VISUALIZATION_GUI_TRIAL or the handle to
%      the existing singleton*.
%
%      DELTA_VISUALIZATION_GUI_TRIAL('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in DELTA_VISUALIZATION_GUI_TRIAL.M with the given input arguments.
%
%      DELTA_VISUALIZATION_GUI_TRIAL('Property','Value',...) creates a new DELTA_VISUALIZATION_GUI_TRIAL or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before delta_visualization_gui_trial_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to delta_visualization_gui_trial_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help delta_visualization_gui_trial

% Last Modified by GUIDE v2.5 08-Aug-2022 10:56:41

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @delta_visualization_gui_trial_OpeningFcn, ...
                   'gui_OutputFcn',  @delta_visualization_gui_trial_OutputFcn, ...
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


% --- Executes just before delta_visualization_gui_trial is made visible.
function delta_visualization_gui_trial_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to delta_visualization_gui_trial (see VARARGIN)

% Choose default command line output for delta_visualization_gui_trial
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes delta_visualization_gui_trial wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = delta_visualization_gui_trial_OutputFcn(hObject, eventdata, handles) 
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
global val; global m; global delta_waveform_broadband_total; global TotalDeltaChunks;
global DeltaSignal; global peaks; global Hippocamp; global Hippocamp_filtered; 
global DeltaFiltered; global delta_timestamps_SD;

addpath(genpath('/home/genzel/Documents/UMAP_Basic_OS/'))
[FileName,path]=uigetfile('*.*','.mat','MultiSelect','on');
waveform=FileName(find(contains(FileName,'waveform')));
timestamps=FileName(find(contains(FileName,'timestamps')));
File=fullfile(path,waveform{1,1});
File2=fullfile(path,timestamps{1,1});
delta_waveform_broadband_total=load(File);
delta_waveform_broadband_total=delta_waveform_broadband_total.delta_waveform_broadband_total;
delta_timestamps_SD=load(File2);
delta_timestamps_SD=delta_timestamps_SD.delta_timestamps_SD;

prompt = {'Select a trial 1(presleep)-2(PT1)-3(PT2)-4(PT3)-5(PT4)-6(PT5.1)-7(PT5.2)-8(PT5.3)-9(PT5.4))'};
dlgtitle = 'Choose between (1-9)';
definput = {'9'};
ChosenPTforRD = inputdlg(prompt,dlgtitle,[1 80],definput); %Chosen PT for Ripple Detection
m=str2double(ChosenPTforRD{1, 1});

TotalDeltaChunks=length(delta_waveform_broadband_total{1, m});  %find detection num
set(handles.text5,'string',TotalDeltaChunks);

msgbox("---- Deltas Succesfully Loaded ---- ");


% --- Executes on slider movement.
function slider2_Callback(hObject, eventdata, handles)
% hObject    handle to slider2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
global val; global m; global delta_waveform_broadband_total; global TotalDeltaChunks;
global DeltaSignal; global peakss; global Hippocamp; global Hippocamp_filtered; 
global DeltaFiltered; global delta_timestamps_SD; global starts;
global finishes; global peaklineLoc; global startlineLoc; global endlineLoc;

fn=2500;

val=get(handles.slider2,'Value');
val=round(val);
set(handles.text4,'string',val);

% set(handles.slider1, 'Min', 2);
set(handles.slider2, 'Max', TotalDeltaChunks+1);
if TotalDeltaChunks>10
    set(handles.slider2, 'SliderStep', [1/(TotalDeltaChunks-2) , 10/(TotalDeltaChunks-2) ]);
else
    set(handles.slider2, 'SliderStep', [0.1/TotalDeltaChunks , 1/TotalDeltaChunks]);
end
DeltaSignal=delta_waveform_broadband_total{1, m}{val, 1}; 
Wn1 = [1/(fn/2) 6/(fn/2)]; % 1-6 Hz
[b2,a2] = butter(3,Wn1,'bandpass'); %Filter coefficients
DeltaFiltered=filtfilt(b2,a2,delta_waveform_broadband_total{1, m}{val, 1});
peakss=[];
uzunluk=size(delta_timestamps_SD{1, m});
for i=1:uzunluk(1)
    peakss=[peakss delta_timestamps_SD{1, m}(i, 2)];
end
peakss=peakss*2500;

starts=[];
for i=1:uzunluk(1)
    starts=[starts delta_timestamps_SD{1, m}(i, 1)];
end
starts=starts*2500;
% 
finishes=[];
for i=1:uzunluk(1)
    finishes=[finishes delta_timestamps_SD{1, m}(i, 3)];
end
finishes=finishes*2500;

if length(DeltaSignal)>10000
    peakpoint=10000+(peakss(val)-starts(val));
    startlineLoc=peakpoint-(peakss(val)-starts(val));
    peaklineLoc= peakpoint;
    endlineLoc=peakpoint+(finishes(val)-peakss(val));
    
    axes(handles.axes2);
    cla;
    
    plot(DeltaFiltered*2.5+1.5*abs(max(DeltaSignal)-min(DeltaFiltered)),'k')
    text(length(DeltaFiltered),mean(DeltaFiltered*2.5+1.5*abs(max(DeltaSignal)-min(DeltaFiltered))),'\leftarrow Filtered')
    hold on
    plot(DeltaSignal,'b')
    text(length(DeltaSignal),mean(DeltaSignal),'\leftarrow Raw')
    
    set(gca,'XTick',0:1000:length(DeltaSignal));
    set(gca,'XTickLabel',0:0.4:length(DeltaSignal)/2500);
    
    xline(startlineLoc,'--');
    xl=xline(peaklineLoc,'--', peakss(val)/2500);
    xl.LabelVerticalAlignment = 'middle';
    xl.LabelHorizontalAlignment = 'center';
    xl.LabelOrientation = 'horizontal';
    xline(endlineLoc,'--');
    
    xlim tight
    hold off
else
    peakpoint=(peakss(val)-starts(val));
    startlineLoc=peakpoint-(peakss(val)-starts(val));
    peaklineLoc= peakpoint;
    endlineLoc=peakpoint+(finishes(val)-peakss(val));
    
    axes(handles.axes2);
    cla;
    
    plot(DeltaFiltered*2.5+1.5*abs(max(DeltaSignal)-min(DeltaFiltered)),'k')
    text(length(DeltaFiltered),mean(DeltaFiltered*2.5+1.5*abs(max(DeltaSignal)-min(DeltaFiltered))),'\leftarrow Filtered')
    hold on
    plot(DeltaSignal,'b')
    text(length(DeltaSignal),mean(DeltaSignal),'\leftarrow Raw')
    
    set(gca,'XTick',0:250:length(DeltaSignal));
    set(gca,'XTickLabel',0:0.1:length(DeltaSignal)/2500);
    
    xline(startlineLoc,'--');
    xl=xline(peaklineLoc,'--', peakss(val)/2500);
    xl.LabelVerticalAlignment = 'middle';
    xl.LabelHorizontalAlignment = 'center';
    xl.LabelOrientation = 'horizontal';
    xline(endlineLoc,'--');
    
    xlim tight
    hold off
end

% --- Executes during object creation, after setting all properties.
function slider2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to slider2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end
