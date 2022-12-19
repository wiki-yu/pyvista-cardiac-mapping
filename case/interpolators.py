from attr import attrs
import numpy as np
import numba
from .case_routines import calculate_distance

__all__ = [
    'LocalSmoothingInterpolator',
]

@attrs(auto_attribs=True, auto_detect=True)
class LocalSMoothingInterpolator:
    """Interpolator for performing local  smoothing.
    Args:
        points (np.ndarray): Mapping points coordinates.
        field (np.ndarray): Scalar values for each mapping point.
        smoothing_length (int): Cutoff distance between `points` and coordinates
            at which the interpolant is evaluated. Typically, values in the range
            5-10 are reasonable. Defaults to 5.
        fill_value (float): Value used to assign to the field at coordinates that
            fall outside the query radius.
    """

    points: np.ndarray
    field: np.ndarray
    # smoothing_length: int = 5
    smoothing_length: int = 10
    fill_value: float = np.NaN

    def __call__(self, new_points):
        """Evaluate the interpolant.
        Args:
            new_points (np.ndarray): Coordinates at which to evaluate the interpolant.
        Returns:
            y (np.ndarray): Interpolated field at `new_points`.
        """

        n_points = len(new_points)
        # print("$$$: new points len: ", n_points)
        # print("$$$: self points len: ", len(self.points))
        new_field = np.full(n_points, fill_value=self.fill_value, dtype=float)

        distances = calculate_distance(
            origin=new_points,
            destination=self.points,
        )
        # print("$$$ distance shape: ", distances.shape)
        # print("distances: ", distances)

        new_field = _local_smoothing(
            field=self.field,
            smoothing_length=self.smoothing_length,
            distances=distances,
            out=new_field,
        )
        return new_field

@numba.jit(nopython=True, cache=True, fastmath=True)
def _local_smoothing(field, smoothing_length, distances, out):

    within_cutoff = distances < smoothing_length
    # print("$$$ within_cutoff len: ", within_cutoff.shape, out.shape[0])
    # print("$$$ within_cutoff: ", within_cutoff)

    for index in range(out.shape[0]):
        # if not any 1366 distance smaller than the threshold, then continue
        if not np.any(within_cutoff[index]):
            # print(within_cutoff[index], index)
            continue
        
        # # Method1: Use the nearest points within the threshold
        # # Calculate field at new points
        # distance = distances[index]
        # # print("dis shape: ", distance.shape)
        # exponent = distance[distance < smoothing_length] / smoothing_length
        # # print("exponent shape: ", exponent.shape)
        # weights = np.exp(-exponent**2)
        # # print("weights shape: ", weights.shape)
        # normalised_weights = weights / weights.sum()
        # # print(normalised_weights)
        # field_value = sum(field[distance < smoothing_length] * normalised_weights)

        # Method2: Use the nearest point
        distance = distances[index]
        # print("distance", distance)
        field_value = field[np.argmin(distance)]
        # print("field_value: ", field_value)

        out[index] = field_value

    return out
