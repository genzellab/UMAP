function [m]=compute_AUC2(x)
if size(x,2)~=127
    x=x.';
end
    if ~ isempty(x)
        for i=1:size(x,1)
            m(i) = trapz((1:size(x(i,:).',1))./2500, abs(x(i,:).')  );
        end

    else
         m=[];
    end
end 
   