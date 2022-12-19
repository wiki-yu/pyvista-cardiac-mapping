import pyvista
import numpy as np
from reader import load_dataset_mat, create_mesh, draw_map
import matplotlib.pyplot as plt
import math
import pandas as pd


def main():
    """
    The main function to specify the workflow
    """
    ## Carto dataset
    # Read the carto EP study data
    filename = "./data/dataset_1.mat"
    points, indices, fields, electric = load_dataset_mat(filename)

    # # # Creating mesh
    # # mesh = create_mesh(points, indices)
    # # vertices = mesh.points
    # # faces = mesh.faces
    # # voltage = [0 if math.isnan(x) else x for x in fields.bipolar_voltage]

    # ## Plot the points cloud
    # cloud = pyvista.PolyData(points)
    # cloud["point_color"] = cloud.points[:, 2]  # just use z coordinate
    # pyvista.plot(cloud, scalars="point_color", cmap="jet", show_bounds=True, cpos="yz")

    # # 3D points VS mapping points
    # pl = pyvista.Plotter()
    # pl.add_points(points, render_points_as_spheres=True, point_size=5.0, color="red")

    # mapping_points = electric.bipolar_egm.points
    # pl.add_points(
    #     mapping_points,
    #     render_points_as_spheres=True,
    #     point_size=5.0,
    #     color="yellow",
    # )
    # pl.show()

    ## Read the electric signals
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

    # Tim's dataset
    # f_points= open("../data/test_surface_mesh.json", "r")
    # data = json.loads(f_points.read())
    # vertices = np.array(data["vertices"])
    # f_meshes= open("test_surface_mesh.json", "r")
    # data = json.loads(f_meshes.read())
    # faces = np.array(data["faces"])
    # faces = np.insert(faces, 0, 3, axis = 1)
    # mesh = pyvista.PolyData(vertices, faces)
    # mesh.plot()

    # mesh = pyvista.PolyData(vertices, faces)
    # plotter = draw_map(
    #     mesh=mesh,
    #     field=voltage,
    # )
    # plotter.show()

    # # Data decimation adjusting resolution
    # target_reduction = 0.9
    # decimated_mesh = mesh.decimate_pro(target_reduction)
    # mesh_points_list = np.array(mesh.points).tolist()
    # decimated_mesh_points_list = np.array(decimated_mesh.points).tolist()

    # index_list = []
    # for item in decimated_mesh_points_list:
    #     if item in mesh_points_list:
    #         index_list.append(mesh_points_list.index(item))
    # print(len(index_list))

    # decimated_voltage = []
    # for index in index_list:
    #     decimated_voltage.append(voltage[index])
    # print(len(decimated_voltage))

    # voltage = voltage[: decimated_mesh.n_points]
    # plotter = draw_map(
    #     mesh=decimated_mesh,
    #     field=decimated_voltage,
    # )
    # plotter.show()


if __name__ == "__main__":
    main()
