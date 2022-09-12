import pyvista as pv
import numpy as np
import json
from pyvista import examples
import collections

# mesh points
vertices = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0.5, 0.5, -1]])

# mesh faces
faces = np.hstack(
    [
        [4, 0, 1, 2, 3],  # square
        [3, 0, 1, 4],  # triangle
        [3, 1, 2, 4],  # triangle
    ]
)

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

# # target_reduction = 0.7
# # pro_decimated = mesh.decimate_pro(target_reduction, preserve_topology=True)
# # pro_decimated.plot(cpos=cpos, **dargs)

# # plot each face with a different color
# decimated_surf.plot(
#     # scalars=np.arange(3),
#     # cpos=[-1, 1, 0.5],
#     # show_scalar_bar=False,
#     # show_edges=True,
#     # line_width=5,
# )

# import pyvista
# sphere = pyvista.Sphere(phi_resolution=60, theta_resolution=60)
# sphere.plot(show_edges=True, line_width=2)
# print(sphere)

# decimated = sphere.decimate_pro(0.1)
# decimated.plot(show_edges=True, line_width=2)
# print(decimated)

# mesh = examples.download_face()

# f_points= open("test_surface_mesh.json", "r")
# data = json.loads(f_points.read())
# vertices = np.array(data["vertices"])

# f_meshes= open("test_surface_mesh.json", "r")
# data = json.loads(f_meshes.read())
# faces = np.array(data["faces"])
# faces = np.insert(faces, 0, 3, axis = 1)

# mesh = pv.read("Heart.obj")  
# # print("mesh: ", mesh)
# # print("vertices: ", mesh.points)
# # counter = collections.Counter(mesh.faces)
# # print(counter)
# vertices = mesh.points
# faces = mesh.faces
# pro_decimated = mesh.decimate_pro(0.9)
# mesh.plot(pro_decimated)
# faces = np.reshape(np.array(mesh.faces).reshape(-1, 5))
# print(faces)

# Define a camera position that shows this mesh properly
# cpos = [(0.4, -0.07, -0.31), (0.05, -0.13, -0.06), (-0.1, 1, 0.08)]
# dargs = dict(show_edges=False, color=True)

# Preview the mesh

# target_reduction = 0.7
# print(f"Reducing {target_reduction * 100.0} percent out of the original mesh")

# decimated = mesh.decimate(target_reduction)

# decimated.plot(**dargs)

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


