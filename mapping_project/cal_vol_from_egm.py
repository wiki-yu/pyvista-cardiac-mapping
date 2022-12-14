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

    return within_woi  # This is now a 2D array that can be used to index into electrograms and calculate voltages.


def calculate_voltage_from_electrograms(
    electric, buffer=50, bipolar=True, indices=None
):
    """
    Calculates the peak-to-peak voltage from electrograms.
    """

    if bipolar:
        electrograms = electric.bipolar_egm.egm.copy()
    else:
        # Unipolar case, Dont need it for now
        # Use only the proximal unipolar data
        electrograms = electric.unipolar_egm.egm[:, :, 0].copy()
    print("### Length of electrograms: ", len(electrograms))

    sample_within_woi = get_sample_indices_within_woi(electric, buffer=buffer)
    print("### Length of sample_within_woi ", sample_within_woi.shape)
    print(sample_within_woi)

    electrograms[~sample_within_woi] = np.NaN

    amplitudes = np.nanmax(electrograms, axis=1) - np.nanmin(electrograms, axis=1)

    return amplitudes


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
    voltage = fields.bipolar_voltage
    mesh = pyvista.PolyData(vertices, faces)

    # # Original Carto formed map
    # plotter = draw_map(
    #     mesh=mesh,
    #     field=voltage,
    # )
    # plotter.show()

    # Our interpolated map
    interpolator_voltage = interpolators.NearestInterpolator(
        points=electric.bipolar_egm.points,
        field=electric.bipolar_egm.voltage,
    )
    interpolated_voltage = interpolator_voltage(new_points=points)
    print("interpolated_voltage: ", interpolated_voltage)

    # # Draw the interpolated map
    # plotter = draw_map(
    #     mesh=mesh,
    #     field=interpolated_voltage,
    # )
    # plotter.show()

    cal_voltages = calculate_voltage_from_electrograms(electric)
    interpolator_cal_voltage = interpolators.NearestInterpolator(
        points=electric.bipolar_egm.points, field=cal_voltages
    )
    interpolated_cal_voltage = interpolator_cal_voltage(new_points=points)

    print("Voltage: ", cal_voltages)
    print("Carto data: ", electric.bipolar_egm.voltage)
    # Draw the interpolated map
    plotter = draw_map(mesh=mesh, field=interpolated_cal_voltage, field_type="voltage")
    plotter.show()

    plt.figure(figsize=(20, 8))
    plt.subplot(2, 1, 1)
    plt.title("Carto data")
    plt.plot(electric.bipolar_egm.voltage, "r-")
    plt.subplot(2, 1, 2)
    plt.title("Calculated data")
    plt.plot(cal_voltages, "b-")
    plt.show()
