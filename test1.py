import pyvista as pv
import numpy as np
import json
from pyvista import examples
import collections

# mesh points
# vertices = np.array([[0, 0, 0], [1, 0, 0], [1, 0.5, 0], [0, 0.5, 0]])
# faces = np.hstack([[3, 0, 1, 2], [3, 0, 3, 2]])


# f_points= open("test_surface_mesh.json", "r")
# data = json.loads(f_points.read())
# vertices = np.array(data["vertices"])

# f_meshes= open("test_surface_mesh.json", "r")
# data = json.loads(f_meshes.read())
# faces = np.array(data["faces"])
# faces = np.insert(faces, 0, 3, axis = 1)

# mesh = pv.PolyData(vertices, faces)
# target_reduction = 0.5
# print("surf: ", surf)
# decimated_surf = surf.decimate(target_reduction)
# print("decimated_surf: ", decimated_surf)

# import trimesh
# mesh = pv.read("heart2.obj") 
# mesh.plot()
# # vertices = mesh.points
# # faces = mesh.faces 

# mesh = trimesh.load('heart2.obj', force='mesh')
# vertices = np.array(mesh.vertices).tolist()
# faces = np.array(mesh.faces + 1).tolist()

# data = {'vertices': vertices, 'faces': faces}
# with open('heart2.json', 'w') as f:
#     json.dump(data, f)


import pyvista
import numpy as np
import json
from reader import load_dataset_mat, create_mesh, draw_map
import matplotlib.cm
import math


def main():
    # filename = "./data/dataset_2.mat"
    # points, indices, fields = load_dataset_mat(filename)
    # mesh = create_mesh(points, indices)
    # vertices = mesh.points
    # faces = mesh.faces
    # voltage = [0 if math.isnan(x) else x for x in fields.bipolar_voltage]


    points = pv.wrap(pv.Sphere().points)
    # new_points = np.array(points).tolist()
    # print("type new points: ", type(new_points))
    print("points: ", points)
    # print("new_points: ", new_points)
    mesh = points.reconstruct_surface()
    new_points = np.array(mesh.points).tolist()
    new_points = new_points[:842]
    cloud = pyvista.PolyData(new_points)
    surf = cloud.delaunay_2d()
    surf.plot(cpos="xy", show_edges=False)
    # new_mesh = new_points.reconstruct_surface()


    # plotter = draw_map(
    #     mesh=new_mesh,
    #     # field=voltage,
    # )
    # plotter.show()


if __name__ == "__main__":
    main()  

# import numpy as np
# import pyvista as pv

# # Define a simple Gaussian surface
# n = 20
# x = np.linspace(-200, 200, num=n) + np.random.uniform(-1, 5, size=n)
# y = np.linspace(-200, 200, num=n) + np.random.uniform(-7, 9, size=n)
# xx, yy = np.meshgrid(x, y)
# A, b = 100, 100
# zz = A * np.exp(-0.5 * ((xx / b) ** 2.0 + (yy / b) ** 2.0))

# # Get the points as a 2D NumPy array (N by 3)
# points = np.c_[xx.reshape(-1), yy.reshape(-1), zz.reshape(-1)]

# noise = np.random.randn(400, 3) * 3
# points_noise = points + noise
# print("points_noise: ", points_noise)


# cloud = pv.PolyData(points_noise)
# # cloud.plot(point_size=15)

# surf = cloud.delaunay_2d()
# surf.plot(show_edges=True)