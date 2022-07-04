function [m]=compute_duration(x)
 if size(x,2)>size(x,1)
     x=x.';
 end
    if ~ isempty(x)
        m=cellfun('length',x)/2500*1000;
%         for i=1:size(x,1)
%             m(i) = trapz((1:size(x(i,:).',1))./2500, abs(x(i,:).')  );
%         end

    else
         m=[];
    end
end 
   