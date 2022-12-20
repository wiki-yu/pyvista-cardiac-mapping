import sys

sys.path.append("../mapping_project")
import pyvista
import numpy as np
from utils.reader import load_dataset_mat, create_mesh, draw_map
import matplotlib.pyplot as plt
import math
import pandas as pd


def main():
    """
    The main function to specify the workflow
    """
    ## Carto dataset
    # Read the carto EP study data
    filename = "../data/dataset_1.mat"
    surface, electric = load_dataset_mat(filename)
    points = surface["points"]
    indices = surface["indices"]
    fields = surface["fields"]

    ## Creating mesh & voltage map visualization
    mesh = create_mesh(points, indices)
    voltage = fields.bipolar_voltage
    plotter = draw_map(mesh=mesh, field=voltage, field_type="voltage")
    plotter.show()

    ## Points cloud visualization
    cloud = pyvista.PolyData(points)
    cloud["point_color"] = cloud.points[:, 2]  # just use z coordinate
    pyvista.plot(cloud, scalars="point_color", cmap="jet", show_bounds=True, cpos="yz")

    # 3D points VS mapping points
    pl = pyvista.Plotter()
    pl.add_points(points, render_points_as_spheres=True, point_size=5.0, color="red")

    mapping_points = electric.bipolar_egm.points
    pl.add_points(
        mapping_points,
        render_points_as_spheres=True,
        point_size=5.0,
        color="yellow",
    )
    pl.show()

    ## Electric signals visualization
    biploar_egm = electric.bipolar_egm.egm
    ref_egm = electric.reference_egm.egm
    ecg = electric.ecg.ecg
    print(np.shape(biploar_egm[0]), np.shape(ref_egm[0]), np.shape(ecg[0]))
    plt.figure(figsize=(15, 7))
    plt.subplot(3, 1, 1)
    plt.title("Bipolar egm")
    plt.plot(biploar_egm[10])
    plt.subplot(3, 1, 2)
    plt.title("Reference egm")
    plt.plot(ref_egm[10])
    plt.subplot(3, 1, 3)
    plt.title("Surface ECG")
    plt.plot(ecg[10])
    plt.show()
    print("### electric.annotations.local_activation_time")
    print(len(electric.annotations.local_activation_time))
    df = pd.DataFrame(electric.annotations.local_activation_time)
    print(df.describe())
    print("*** electric.annotations.local_activation_time > 0")
    pos_lat = [val for val in electric.annotations.local_activation_time if val > 0]
    df2 = pd.DataFrame(pos_lat)
    print(df2.describe())
    print("@@@ surface.local_activation_time")
    pos_lat = [val for val in fields.local_activation_time if val > 0]
    df3 = pd.DataFrame(pos_lat)
    print(df3.describe())


if __name__ == "__main__":
    main()
