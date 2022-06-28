function [m]=compute_amplitude_liset(x)
  if size(x,2)~=127
    x=x.';
end

    if ~ isempty(x)
        for i=1:size(x,1)
            m(i)=URC_compute_ampLabel(x(i,:),2500);
        end

    else
         m=[];
    end
end 
   