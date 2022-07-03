# List of features

## Hippocampal ripples features.
- Amplitude :heavy_check_mark:
```
 %% Amplitude
 ripple_amp=cellfun(@(x) max(abs(hilbert(x.'))) ,T.Ripples,'UniformOutput',false);

 T=[T ripple_amp];
 T.Properties.VariableNames(6)={'Amplitude'};
 ```
- Mean frequency :heavy_check_mark:
```
 %% Mean Freq
[ripple_meanfreq]=cellfun(@(x) (compute_meanfreq(x)) ,T.Ripples,'UniformOutput',false);

 T=[T ripple_meanfreq];
 T.Properties.VariableNames(7)={'Mean frequency'};
 ```
- Amplitude (2nd method)
```
[ripple_amp2]=cellfun(@(x) (compute_amplitude_liset(x)) ,T.Ripples,'UniformOutput',false);

T=[T ripple_amp2];
T.Properties.VariableNames(8)={'Amplitude2'};
```
- Frequency (2nd method)
```
[ripple_freq]=cellfun(@(x) (compute_frequency_liset(x)) ,T.Ripples,'UniformOutput',false);

T=[T ripple_freq];
T.Properties.VariableNames(9)={'Frequency'};
```
- Entropy
```
[ripple_ent]=cellfun(@(x) (compute_entropy(x)) ,T.Ripples,'UniformOutput',false);

T=[T ripple_ent];
T.Properties.VariableNames(10)={'Entropy'};
```
- AUC
```
[ripple_auc]=cellfun(@(x) (compute_AUC(x)) ,T.Ripples,'UniformOutput',false);

T=[T ripple_auc];
T.Properties.VariableNames(11)={'AUC'};
```

- Duration
