function [amp] = URC_compute_ampLabel(alignedFiltRipples, fs)
%    amp = max(abs(alignedFiltRipples(:,round(size(alignedFiltRipples, 2)/2)-50:round(size(alignedFiltRipples, 2)/2)+50)), [], 2);
    offset = round(0.002 * fs);
    amp = max(abs(alignedFiltRipples(:,round(size(alignedFiltRipples, 2)/2)-offset:round(size(alignedFiltRipples, 2)/2)+offset)), [], 2);
end
