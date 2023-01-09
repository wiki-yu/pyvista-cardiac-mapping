import numpy as np


class FeatureCal:
    def __init__(self, egm, woi, ref_annotations, buffer=50):
        self.egm = egm
        self.woi = woi
        self.ref_annotations = ref_annotations
        self.buffer = buffer

    def get_sample_indices_within_woi(self):
        """
        Determine which samples are within the window of interest for each electrogram.
        """
        egm = self.egm
        woi = self.woi
        ref_annotations = self.ref_annotations
        buffer = self.buffer

        sample_indices = np.full_like(
            egm, fill_value=np.arange(egm.shape[1]), dtype=int
        )
        start_time, stop_time = (woi + ref_annotations + [-buffer, buffer]).T

        within_woi = np.logical_and(
            sample_indices >= start_time[:, np.newaxis],
            sample_indices <= stop_time[:, np.newaxis],
        )
        return within_woi

    def calculate_lat_from_electrograms(self):
        """
        Calculates LAT from electrograms with the info of WOI and ref.
        """
        egm = self.egm
        sample_within_woi = self.get_sample_indices_within_woi()

        egm[~sample_within_woi] = 0
        max_idx = np.argmax(egm, axis=1)

        return max_idx

    def calculate_voltage_from_electrograms(self):
        """
        Calculates the peak-to-peak voltage from electrograms.
        """
        egm = self.egm
        sample_within_woi = self.get_sample_indices_within_woi()

        egm[~sample_within_woi] = np.NaN

        amplitudes = np.nanmax(egm, axis=1) - np.nanmin(egm, axis=1)

        return amplitudes
