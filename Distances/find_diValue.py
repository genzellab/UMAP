import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 


df = pd.read_excel("/home/irene/Documents/UMAP/latest_data.xlsx", usecols="C,D,E,F,G,H,I")


def value_cmp(string,value):
    Amp=[];
    for i in range(df.shape[0]):
        #print(i);
        if df.loc[i][string]==value:
            Amp.append(1)
        else:
            Amp.append(0)
    A=np.array(Amp)       
    return A



trialsArray=[value_cmp("trial", 1),value_cmp("trial", 2),value_cmp("trial", 3),
             value_cmp("trial", 4),value_cmp("trial", 5),value_cmp("trial", 6)]

ratsArray=[value_cmp("subject", 1),value_cmp("subject", 2),value_cmp("subject", 6),
           value_cmp("subject", 9),value_cmp("subject", 3),value_cmp("subject", 4),
           value_cmp("subject", 7),value_cmp("subject", 8)]

daysArray=[value_cmp("condition.1", "or"),value_cmp("condition.1", "od"),value_cmp("condition.1", "con")]

arrayDI=[df.loc[:,"DI_5min"],df.loc[:,"DI_10min"]]

def find_logic(rat, day, trial):
    K=[]
    
    for i in range(len(rat)):
        for j in range(len(day)):
            for k in range(len(trial)):
                logicresult=rat[i]*day[j]*trial[k]
                K.append(logicresult)    
    
    return K


def outputDI():
    res=[]
    logicresult=find_logic(ratsArray, daysArray,trialsArray)
    for i in range(144):
        for j in range(144):
            if (logicresult[i][j]==1):
                if (j < 120):
                    result = arrayDI[0][j]
                else:
                    result = arrayDI[1][j]
                res.append(result)
    return res

outputDI()
