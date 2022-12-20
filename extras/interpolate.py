import pyvista
import numpy as np
from reader import load_dataset_mat, create_mesh, draw_map
import matplotlib.pyplot as plt
import math
import pandas as pd
from kd_tree_nearest import KDTree


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

    # Carto projected & interpolated data
    lat = fields.local_activation_time
    # df = pd.DataFrame(voltage, columns=['vol'])
    # count_nan = df['vol'].isnull().sum()
    # print("nan value amount: ", count_nan)
    # print(df.describe())
    # print("voltage: ", voltage)
    
    # Carto data plot
    mesh = pyvista.PolyData(vertices, faces)
    plotter = draw_map(
        mesh=mesh,
        field=lat,
    )
    plotter.show()


    # mapping_points = electric.bipolar_egm.points
    # kdtree = KDTree(points.tolist())
    # proj_points = []
    # for point in mapping_points:
    #     dist, proj_point = kdtree.find_nearest(point)
    #     proj_points.append(proj_point)

    # # print("projected points: ", proj_points)
    # # print("surface 3d points: ", points)
    
    # for p in proj_points:
    #     if p in points:
    #         print("True")
    #     else:
    #         print("no")


if __name__ == "__main__":
    main()
