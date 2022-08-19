function varargout = ripple_vis_gui_trial(varargin)
% RIPPLE_VIS_GUI_TRIAL MATLAB code for ripple_vis_gui_trial.fig
%      RIPPLE_VIS_GUI_TRIAL, by itself, creates a new RIPPLE_VIS_GUI_TRIAL or raises the existing
%      singleton*.
%
%      H = RIPPLE_VIS_GUI_TRIAL returns the handle to a new RIPPLE_VIS_GUI_TRIAL or the handle to
%      the existing singleton*.
%
%      RIPPLE_VIS_GUI_TRIAL('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in RIPPLE_VIS_GUI_TRIAL.M with the given input arguments.
%
%      RIPPLE_VIS_GUI_TRIAL('Property','Value',...) creates a new RIPPLE_VIS_GUI_TRIAL or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before ripple_vis_gui_trial_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to ripple_vis_gui_trial_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help ripple_vis_gui_trial

% Last Modified by GUIDE v2.5 21-Jul-2022 14:01:14

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @ripple_vis_gui_trial_OpeningFcn, ...
                   'gui_OutputFcn',  @ripple_vis_gui_trial_OutputFcn, ...
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


% --- Executes just before ripple_vis_gui_trial is made visible.
function ripple_vis_gui_trial_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to ripple_vis_gui_trial (see VARARGIN)

% Choose default command line output for ripple_vis_gui_trial
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes ripple_vis_gui_trial wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = ripple_vis_gui_trial_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global val; global m; global GC_window_ripples_broadband_total; global TotalRipChunks;
global RippleSignal; global Cortex; global Hippocamp; global Hippocamp_filtered; 
global Cortex_filtered; 

addpath(genpath('/home/genzel/Documents/UMAP_Basic_OS/'))

[GCName,path]=uigetfile('GC_window_ripples_broadband*.mat');
File=fullfile(path,GCName)
GC_window_ripples_broadband=load(File);
GC_window_ripples_broadband_total=GC_window_ripples_broadband.GC_window_ripples_broadband_total;

prompt = {'Select a trial 1(presleep)-2(PT1)-3(PT2)-4(PT3)-5(PT4)-6(PT5.1)-7(PT5.2)-8(PT5.3)-9(PT5.4))'};
dlgtitle = 'Choose between (1-9)';
definput = {'9'};
ChosenPTforRD = inputdlg(prompt,dlgtitle,[1 80],definput); %Chosen PT for Ripple Detection
m=str2double(ChosenPTforRD{1, 1});

TotalRipChunks=length(GC_window_ripples_broadband_total{1, m});  %find detection num
set(handles.text4,'string',TotalRipChunks);

msgbox("----- Files Loaded ---- ");

% --- Executes on slider movement.
function slider1_Callback(hObject, eventdata, handles)
% hObject    handle to slider1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
global val; global m; global GC_window_ripples_broadband_total; global TotalRipChunks;
global RippleSignal; global Cortex; global Hippocamp; global Hippocamp_filtered; 
global Cortex_filtered; 
fn=2500;

val=get(handles.slider1,'Value');
val=round(val);
set(handles.text2,'string',val);

% set(handles.slider1, 'Min', 2);
set(handles.slider1, 'Max', TotalRipChunks);
set(handles.slider1, 'SliderStep', [1/(TotalRipChunks-2) , 10/(TotalRipChunks-2) ]);

fn=2500;
RippleSignal=GC_window_ripples_broadband_total{1, m}{val, 1}; 
Cortex=RippleSignal(1,:);
Hippocamp=RippleSignal(2,:);
Wn1=[100/(fn/2) 300/(fn/2)]; % Cutoff=100-300 Hz
[b1,a1] = butter(3,Wn1,'bandpass');
Hippocamp_filtered= filtfilt(b1,a1,Hippocamp);
Wn2=[0.5/(fn/2) 20/(fn/2)]; 
[b2,a2] = butter(3,Wn2,'bandpass'); %Filter coefficients
Cortex_filtered=filtfilt(b2,a2,Cortex);

StartP=GC_window_ripples_broadband_total{1, m}{val, 2}  *2500 ;
PeakP=GC_window_ripples_broadband_total{1, m}{val, 3}*2500 ;
EndP=GC_window_ripples_broadband_total{1, m}{val, 4}*2500 ;
startlineLoc=7501-(PeakP-StartP);
peaklineLoc= 7501;
endlineLoc=7501+(EndP-PeakP);
axes(handles.axes1);
cla;

plot(Hippocamp_filtered*6+2.4*abs(max(Cortex_filtered)-min(Hippocamp_filtered)),'b')
text(length(Hippocamp_filtered),mean(Hippocamp_filtered*6+2.4*abs(max(Cortex_filtered)-min(Hippocamp_filtered))),'\leftarrow Filtered HPC')
hold on
plot(Cortex_filtered,'k')
text(length(Cortex_filtered),mean(Cortex_filtered),'\leftarrow Filtered PFC')
hold on
plot(Hippocamp-1.7*abs(max(Cortex_filtered)-min(Cortex_filtered)),'b')
text(length(Hippocamp),mean(Hippocamp-1.7*abs(max(Cortex_filtered)-min(Cortex_filtered))),'\leftarrow Raw HPC')
hold on
plot(Cortex-1.5*abs(max(Cortex_filtered)-min(Cortex_filtered))-2*abs(max(Hippocamp)-min(Hippocamp)),'k')
text(length(Cortex),mean(Cortex-1.5*abs(max(Cortex_filtered)-min(Cortex_filtered))-2*abs(max(Hippocamp)-min(Hippocamp))),'\leftarrow Raw PFC')
hold on
a=GC_window_ripples_broadband_total{1, m}(:,7);
b=max(cell2mat(a));
yl=yline(2.4*abs(max(Cortex_filtered)-min(Hippocamp_filtered))+b,'-',b);


set(gca,'XTick',0:500:15000);
set(gca,'XTickLabel',0:0.2:6);

xline(startlineLoc,'--');
xl=xline(peaklineLoc,'--', GC_window_ripples_broadband_total{1, m}{val, 3});
xl.LabelVerticalAlignment = 'middle';
xl.LabelHorizontalAlignment = 'center';
xl.LabelOrientation = 'horizontal';
xline(endlineLoc,'--');
% title(['Event Number is: ' num2str(val),'. for trial' num2str(m) ' of Rat' File(38)...
%    '-'  File(end-5:end-4)])
xlim ([6000 9000]);
hold off

% --- Executes during object creation, after setting all properties.
function slider1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to slider1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end
