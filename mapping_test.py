import pyvista
import numpy as np
from reader import load_dataset_mat
from kd_tree_nearest import KDTree


def main():
    """
    The main function to specify the workflow
    """
    ## Carto dataset
    # Read the carto EP study data
    filename = "./data/dataset_1.mat"
    points, indices, fields, electric = load_dataset_mat(filename)

    # 3D points VS mapping points
    pl = pyvista.Plotter()
    # pl.add_points(points, render_points_as_spheres=True, point_size=5.0, color="red")

    mapping_points = electric.bipolar_egm.points
    print("type mapping points: ", type(mapping_points))

    pl.add_points(
        mapping_points,
        render_points_as_spheres=True,
        point_size=5.0,
        color="yellow",
    )

    kdtree = KDTree(points.tolist())
    proj_points = []
    for point in mapping_points:
        dist, proj_point = kdtree.find_nearest(point)
        proj_points.append(proj_point)

    pl.add_points(
        np.array(proj_points),
        render_points_as_spheres=True,
        point_size=5.0,
        color="white",
    )

    pl.show()


if __name__ == "__main__":
    main()
