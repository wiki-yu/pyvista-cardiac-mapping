from attr import attrs
import numpy as np
import scipy.interpolate


@attrs(auto_attribs=True, auto_detect=True)
class NearestInterpolator:
    """Interpolator based on the nearest points.
    Args:
        points (np.ndarray): Mapping points coordinates.
        field (np.ndarray): Scalar values for each mapping point.
        th (int): Threshold. Nomarlly set between 5~10
        fill_value (float): Value used to assign to the field if fall outside the query radius.
    """

    points: np.ndarray
    field: np.ndarray
    th: int = 10
    fill_value: float = np.NaN

    def __call__(self, new_points):
        """Evaluate the interpolant.
        Args: new_points (np.ndarray): Coordinates at which to evaluate the interpolant.
        Returns: y (np.ndarray): Interpolated field at `new_points`.
        """
        n_points = len(new_points)
        # print("new points len: ", n_points)  # 9279
        # print("self points len: ", len(self.points))  # 1366
        new_field = np.full(n_points, fill_value=self.fill_value, dtype=float)

        distances = calculate_distance(
            origin=new_points,
            destination=self.points,
        )
        # print("Distance matrix shape: ", distances.shape)  # (9279, 1366)

        new_field = generate_data(
            field=self.field,
            th=self.th,
            distances=distances,
            out=new_field,
        )
        return new_field


def calculate_distance(origin, destination):
    """
    Returns the distance from two set of points
    Args:
        origin (ndarray): Nx3 matrix of coordinates
        destination (ndarray): Mx3 matrix of coordinates
    Returns:
        distances (ndarray): MxN matrix of distances
    """

    origin = origin[np.newaxis, :] if origin.ndim == 1 else origin
    destination = destination[np.newaxis, :] if destination.ndim == 1 else destination

    distances = scipy.spatial.distance.cdist(
        origin,
        destination,
    )

    return distances


def generate_data(field, th, distances, out):

    within_cutoff = distances < th

    for index in range(out.shape[0]):
        # if not any 1366 distance smaller than the threshold, then continue
        if not np.any(within_cutoff[index]):
            # print(within_cutoff[index], index)
            continue

        # # Method1: Use the nearest points within the threshold
        # # Calculate field at new points
        # distance = distances[index]
        # # print("dis shape: ", distance.shape)
        # exponent = distance[distance < th] / th
        # # print("exponent shape: ", exponent.shape)
        # weights = np.exp(-exponent**2)
        # # print("weights shape: ", weights.shape)
        # normalised_weights = weights / weights.sum()
        # # print(normalised_weights)
        # field_value = sum(field[distance < th] * normalised_weights)

        # Method2: Use the nearest point
        distance = distances[index]
        field_value = field[np.argmin(distance)]
        # print("field_value: ", field_value)

        out[index] = field_value

    return out
