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

    # Creating mesh
    mesh = create_mesh(points, indices)
    vertices = mesh.points
    faces = mesh.faces


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


    mesh = pyvista.PolyData(vertices, faces)
    plotter = draw_map(
        mesh=mesh
    )
    plotter.show()

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
