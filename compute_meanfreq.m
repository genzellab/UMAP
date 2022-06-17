function [m]=compute_meanfreq(x)
if size(x,2)~=127
    x=x.';
end

    if ~ isempty(x)
        for i=1:size(x,1)
            m(i)=meanfreq(x(i,:),2500);
        end

    else
         m=[];
    end


end