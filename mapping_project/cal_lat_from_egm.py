import numpy as np
import pyvista
from utils.reader import load_dataset_mat, create_mesh, draw_map
from utils import interpolators
import matplotlib.pyplot as plt


def get_sample_indices_within_woi(electric, buffer=50):
    """
    Determine which samples are within the window of interest for each electrogram.
    """
    egm = electric.bipolar_egm.egm
    woi = electric.annotations.window_of_interest
    ref_annotations = electric.annotations.reference_activation_time[:, np.newaxis]

    sample_indices = np.full_like(egm, fill_value=np.arange(egm.shape[1]), dtype=int)
    start_time, stop_time = (woi + ref_annotations + [-buffer, buffer]).T

    within_woi = np.logical_and(
        sample_indices >= start_time[:, np.newaxis],
        sample_indices <= stop_time[:, np.newaxis],
    )
    return within_woi


def calculate_lat_from_electrograms(electric, buffer=50, bipolar=True, indices=None):
    """
    Calculates LAT from electrograms with the info of WOI and ref.
    """

    electrograms = electric.bipolar_egm.egm.copy()
    print("### Length of electrograms: ", len(electrograms))

    sample_within_woi = get_sample_indices_within_woi(electric, buffer=buffer)
    print("### Length of sample_within_woi ", sample_within_woi.shape)

    electrograms[~sample_within_woi] = 0
    max_idx = np.argmax(electrograms, axis=1)

    # print("max index: ", max_idx)
    # original = electric.annotations.local_activation_time
    # original = [i if i >0 else 2000 for i in original]
    # # print("lat: ", original)

    # plt.figure(figsize=(20, 8))
    # plt.subplot(2, 1, 1)
    # plt.plot(max_idx, 'r-')
    # plt.subplot(2, 1, 2)
    # plt.plot(original, 'b-')
    # plt.show()

    return max_idx


if __name__ == "__main__":
    ## Read the dataset
    filename = "../data/dataset_1.mat"
    surface, electric = load_dataset_mat(filename)
    points = surface["points"]
    indices = surface["indices"]
    fields = surface["fields"]

    mesh = create_mesh(points, indices)
    vertices = mesh.points
    faces = mesh.faces
    carto_lat = fields.local_activation_time

    mesh = pyvista.PolyData(vertices, faces)

    # # Original Carto formed map
    # plotter = draw_map(
    #     mesh=mesh,
    #     field=carto_lat,
    #     field_type="lat"
    # )
    # plotter.show()

    # LAT calculated from annotation
    anno_lat = (
        electric.annotations.local_activation_time
        - electric.annotations.reference_activation_time
    )
    print("### anno_lat: ", anno_lat)
    interpolator_lat = interpolators.NearestInterpolator(
        points=electric.bipolar_egm.points, field=anno_lat
    )
    interpolated_lat = interpolator_lat(new_points=points)
    # Draw the interpolated map
    plotter = draw_map(mesh=mesh, field=interpolated_lat, field_type="lat")
    plotter.show()

    # LAT calculated from ECG & EGM feature detection algorithm
    local_activation_time = calculate_lat_from_electrograms(electric)
    cal_lat = local_activation_time - electric.annotations.reference_activation_time
    print("### cal_lat: ", cal_lat)

    interpolator_cal_lat = interpolators.NearestInterpolator(
        points=electric.bipolar_egm.points, field=cal_lat
    )
    interpolated_cal_lat = interpolator_cal_lat(new_points=points)

    # Draw the interpolated map
    plotter = draw_map(mesh=mesh, field=carto_lat, field_type="lat")
    plotter.show()

    print("carto data: ", carto_lat)
    print("interpolated_lat: ", interpolated_lat)
    print("interpolated_cal_lat: ", interpolated_cal_lat)

    plt.figure(figsize=(20, 8))
    plt.subplot(2, 1, 1)
    plt.plot(interpolated_lat, "r-")
    plt.subplot(2, 1, 2)
    plt.plot(interpolated_cal_lat, "b-")
    plt.show()
