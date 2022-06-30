function [amp]=compute_amplitude_Kopal(x)
        for i=1:size(x,1)
            if ~isempty(x{i,:}) 
            amp{i} = URC_compute_ampLabel(x{i,:},2500);
            else 
                amp{i} = {};
            end 
        end
 amp = amp.';
end 
   
