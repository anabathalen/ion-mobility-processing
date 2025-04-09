def fit_with_fixed_stddev(x_data, y_data, peaks):
    # Start by fitting the first peak
    initial_guess = [max(y_data), peaks[0], 100]
    try:
        popt, _ = curve_fit(gaussian, x_data, y_data, p0=initial_guess)
    except Exception as e:
        st.warning(f"Fitting failed for the first peak: {e}")
        return []  # Return empty list if fitting fails for the first peak

    # Extract the fitted standard deviation for the first peak
    stddev_first_peak = popt[2]

    # For subsequent peaks, limit the stddev to be no more than 10% larger than the previous one
    all_params = []
    for i, peak in enumerate(peaks):
        if i == 0:
            # Use the fitted stddev for the first peak
            stddev = stddev_first_peak
        else:
            # For subsequent peaks, limit the stddev to 10% larger than the previous one
            stddev = min(stddev_first_peak * (1 + 0.1 * i), stddev_first_peak * 1.5)  # Arbitrary upper limit of 1.5 times
        
        initial_guess = [max(y_data), peak, stddev]
        try:
            popt, _ = curve_fit(gaussian, x_data, y_data, p0=initial_guess)
            # Append the mean and stddev of each peak (amp is not needed here)
            all_params += popt[1:]  # Ensure we are getting only the "mean" and "stddev"
        except Exception as e:
            st.warning(f"Fitting failed for peak {i+1}: {e}")
            continue  # Skip this peak if fitting fails

    return all_params


