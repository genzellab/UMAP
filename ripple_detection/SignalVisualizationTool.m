function varargout = SignalVisualizationTool(varargin)
% SIGNALVISUALIZATIONTOOL MATLAB code for SignalVisualizationTool.fig
%      SIGNALVISUALIZATIONTOOL, by itself, creates a new SIGNALVISUALIZATIONTOOL or raises the existing
%      singleton*.
%
%      H = SIGNALVISUALIZATIONTOOL returns the handle to a new SIGNALVISUALIZATIONTOOL or the handle to
%      the existing singleton*.
%
%      SIGNALVISUALIZATIONTOOL('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in SIGNALVISUALIZATIONTOOL.M with the given input arguments.
%
%      SIGNALVISUALIZATIONTOOL('Property','Value',...) creates a new SIGNALVISUALIZATIONTOOL or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before SignalVisualizationTool_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to SignalVisualizationTool_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help SignalVisualizationTool

% Last Modified by GUIDE v2.5 22-Jul-2022 13:15:59

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @SignalVisualizationTool_OpeningFcn, ...
                   'gui_OutputFcn',  @SignalVisualizationTool_OutputFcn, ...
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


% --- Executes just before SignalVisualizationTool is made visible.
function SignalVisualizationTool_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to SignalVisualizationTool (see VARARGIN)

% Choose default command line output for SignalVisualizationTool
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes SignalVisualizationTool wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = SignalVisualizationTool_OutputFcn(hObject, eventdata, handles) 
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
global states; global HippoCamp_NREM; global CORTEX_NREM;
global filt_cortex; global filt_hippocamp;  global fn;
global val; global TotalLength;
global File; global EEGFileName;

addpath(genpath('/home/genzel/Documents/'))
[EEGFileName,path]=uigetfile('*.*','.mat','MultiSelect','on');
cd(path)
fn=2500;
HippoCamp=EEGFileName(find(contains(EEGFileName,'HPC')))
File=fullfile(path,HippoCamp{1,1})
HippoCamp=load(File);
HippoCamp=HippoCamp.HPC;
         
CORTEX=EEGFileName(find(contains(EEGFileName,'PFC')))
File=fullfile(path,CORTEX{1,1})
CORTEX=load(File);
CORTEX=CORTEX.PFC;


states=EEGFileName(find(contains(EEGFileName,'state')))
File2=fullfile(path,states{1,1})
states=load(File2);
states=states.states;
ti_main= [0:length(HippoCamp)-1]*(1/fn);
ti_mainPFC= [0:length(CORTEX)-1]*(1/fn);
e_t=1;
e_samples=e_t*(fn); %fs=2500Hz
ch=length(HippoCamp);
ch2=length(CORTEX);
nc=floor(ch/e_samples); %Number of epochsw
nc2=floor(ch2/e_samples);
NC=[];
NC_ti_main=[];
NCPFC=[];
NC_ti_mainPFC=[];
for kk=1:nc
    NC(:,kk)= HippoCamp(1+e_samples*(kk-1):e_samples*kk);
    NC_ti_main(:,kk)= ti_main(1+e_samples*(kk-1):e_samples*kk);
end
for kk=1:nc2
    NCPFC(:,kk)= CORTEX(1+e_samples*(kk-1):e_samples*kk);
    NC_ti_mainPFC(:,kk)= ti_mainPFC(1+e_samples*(kk-1):e_samples*kk);
end
%Find if epoch is NREM (state=3)
vec_bin=states;
vec_bin(vec_bin~=3)=0;
vec_bin(vec_bin==3)=1;
%Cluster one values:
v2=ConsecutiveOnes(vec_bin);
v_index=find(v2~=0);
v_values=v2(v2~=0);
%Extract NREM epochs    
for epoch_count=1:length(v_index)
    v{epoch_count,1}=reshape(NC(:, v_index(epoch_count):v_index(epoch_count)+(v_values(1,epoch_count)-1)), [], 1);
    v_ti{epoch_count,1}=reshape(NC_ti_main(:, v_index(epoch_count):v_index(epoch_count)+(v_values(1,epoch_count)-1)), [], 1);
end
for epoch_count=1:length(v_index)
    vPFC{epoch_count,1}=reshape(NCPFC(:, v_index(epoch_count):v_index(epoch_count)+(v_values(1,epoch_count)-1)), [], 1);
    v_tiPFC{epoch_count,1}=reshape(NC_ti_mainPFC(:, v_index(epoch_count):v_index(epoch_count)+(v_values(1,epoch_count)-1)), [], 1);
end            
HippoCamp_NREM=cat(1,v{:});
CORTEX_NREM=cat(1,vPFC{:}); %raw signals
[c,d] = butter(3, [2/1250 20/1250]);
[e,f] = butter(3, [100/1250 300/1250]);
filt_cortex = filtfilt(c,d, CORTEX_NREM);
filt_hippocamp = filtfilt(e,f, HippoCamp_NREM);

msgbox("----- Files Loaded ---- ");

% --- Executes on slider movement.
function slider1_Callback(hObject, eventdata, handles)
% hObject    handle to slider1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
global states; global HippoCamp_NREM; global CORTEX_NREM;
global filt_cortex; global filt_hippocamp;  global fn; global val;
global TotalLength; global File; global EEGFileName;
fn=2500;

val=get(handles.slider1,'Value');
val=round(val);
set(handles.text3,'string',val);

% set(handles.text2,'string',val);
set(handles.slider1, 'Min', 0);
TotalLength=length(filt_cortex)/15000;
set(handles.text6,'string',TotalLength);

set(handles.slider1, 'Max', TotalLength);
set(handles.slider1, 'SliderStep', [1/(TotalLength-2) , 10/(TotalLength-2) ]);

fn=2500;
axes(handles.axes1);
cla;
filt_hippocamp1=filt_hippocamp((15000*val+1:15000*(val+1)));
filt_cortex1=filt_cortex((15000*val+1:15000*(val+1)));
HippoCamp_NREM1=HippoCamp_NREM((15000*val+1:15000*(val+1)));
CORTEX_NREM1=CORTEX_NREM((15000*val+1:15000*(val+1)));

plot(filt_hippocamp1*6+2.4*abs(max(filt_cortex1)-min(filt_hippocamp1)),'b')
text(length(filt_hippocamp1),mean(filt_hippocamp1*6+2.4*abs(max(filt_cortex1)-min(filt_hippocamp1))),'\leftarrow Filtered HPC')
hold on
plot(filt_cortex1,'k')
text(length(filt_cortex1),mean(filt_cortex1),'\leftarrow Filtered PFC')
hold on
plot(HippoCamp_NREM1-1.7*abs(max(filt_cortex1)-min(filt_cortex1)),'b')
text(length(HippoCamp_NREM1),mean(HippoCamp_NREM1-1.7*abs(max(filt_cortex1)-min(filt_cortex1))),'\leftarrow Raw HPC')
hold on
plot(CORTEX_NREM1-1.5*abs(max(filt_cortex1)-min(filt_cortex1))-2*abs(max(HippoCamp_NREM1)-min(HippoCamp_NREM1)),'k')
text(length(CORTEX_NREM1),mean(CORTEX_NREM1-1.5*abs(max(filt_cortex1)-min(filt_cortex1))-2*abs(max(HippoCamp_NREM1)-min(HippoCamp_NREM1))),'\leftarrow Raw PFC')
hold on
set(gca,'XTick',0:500:15000)
set(gca,'XTickLabel',0:0.2:6)
set(handles.text4,'string',['Chunk Num is: ' num2str(val),'. for ' num2str(EEGFileName{1, 3}(1:12)) ' of Rat' File(38)...
   ' SD -'  File(39:42)]);

xlim tight
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
