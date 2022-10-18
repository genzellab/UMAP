function [Z]=zscore_umap(Y_filtered)

    Data=[];
    for i=1:length(Y_filtered)
        data=Y_filtered{i};
        Data=[Data; data];
    end
    size(Data);
    sum(cellfun('length',Y_filtered));

    SD=(std(Data(:))); %Standard deviation of ripples of that day.
    Z=cellfun(@(x)  (x-mean(x,2))/SD ,Y_filtered,'UniformOutput',false  );

end