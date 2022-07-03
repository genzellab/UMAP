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
- Frequency (2nd method)
- Entropy
- AUC
- Duration
