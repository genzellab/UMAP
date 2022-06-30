function [m]=compute_entropy(x)
  if size(x,2)~=127
    x=x.';
end

    if ~ isempty(x)
        for i=1:size(x,1)
            m(i)=entropy(x(i,:));
        end

    else
         m=[];
    end
end 
   
