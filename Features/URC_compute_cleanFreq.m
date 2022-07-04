function prefFreq = URC_compute_cleanFreq(alignedRipples, Fs)

    prefFreq = nan(size(alignedRipples, 1), 1);
    prefPower = nan(size(alignedRipples, 1), 1);
    for ii = 1:size(alignedRipples, 1)

        event = alignedRipples(ii,:);
        nZeros = round((Fs*(200/1000) - length(event))/2);
        event = [zeros(1, nZeros) event zeros(1, nZeros)];

        % Compute power spectrum
        %[pS, freqs] = power_spectrum( event, true, Fs, [70,500] );
        [pS,freqs] = pspectrum(event,Fs);
        % If maximum power is 70Hz, find if there is another maximum
        if max(pS) == pS(1)
            [~, peaks] = findpeaks(pS);
            peaks(peaks==1) = [];
            if ~isempty(peaks)
                [maxpS, maxfreq] = max(pS(peaks));
                prefPower(ii) = maxpS;
                if peaks(maxfreq) <= length(freqs)
                    maxfreq = freqs(peaks(maxfreq));
                    prefFreq(ii) = maxfreq;
                else
                    prefFreq(ii) = freqs(1);
                end
            else
                prefFreq(ii) = freqs(1);
                prefPower(ii) = pS(1);
            end

        % If maximum power other than 70Hz
        else
            pS = pS(1:end-1);
            [ ~, imax] = max(pS);
            if ~isempty(freqs(imax))
                prefFreq(ii) = freqs(imax);
                prefPower(ii) = pS(imax);
            end
        end

    end
end
