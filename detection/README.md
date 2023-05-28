# Ripple detections scripts

## Detection script
To detect ripples run:

```
swrAnalysiswithPFC.m
```
You may need to adapt the values of k and j depending on the Rat and Study day you want to run.

## Visualization scripts
 - ripple_vis_gui_trial.m 
   Use this script to visualize the ripple detections.
   
 - SignalVisualizationTool.m 
   Use this script to visualize the __concatenated NREM signal__ independently of detections. Useful when there are no detections found. 

 - delta_visualization_gui_trial.m 
   Use this script to visualize the delta detections. 

 - spindle_visualization_gui_trial.m 
   Use this script to visualize the spindle detections. 

## Ripple Characteristics
 -  ripple_characteristics.m 
    Generates excel sheet tables per rat containing the ripple characteristics. 

## Long Short Ripples
 - long_short_ripples. m
   Computes the count of short and long ripples. 
