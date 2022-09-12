import pyvista
import numpy as np
import json
from reader import load_dataset_mat, create_mesh, draw_map
import matplotlib.cm
import math


def main():
    """
    The main function to specify the workflow
    """
    filename = "./data/dataset_2.mat"
    points, indices, fields = load_dataset_mat(filename)
    mesh = create_mesh(points, indices)
    vertices = mesh.points
    faces = mesh.faces

    # voltage = fields.bipolar_voltage
    voltage = [0 if math.isnan(x) else x for x in fields.bipolar_voltage]

    # f_points= open("sample_mesh_reduced_0_05.json", "r")
    # data = json.loads(f_points.read())
    # vertices = np.array(data["vertices"])

    # f_meshes= open("sample_mesh_reduced_0_05.json", "r")
    # data = json.loads(f_meshes.read())
    # faces = np.array(data["faces"])
    # faces = np.insert(faces, 0, 3, axis = 1)

    # print("vertices: ", vertices)
    # print("faces: ", faces)
    


    # After listed, plot not showing
    vertices = points.tolist()
    faces = indices.tolist()
    # mesh = pyvista.PolyData(vertices, faces)
    # ind = mesh.surface_indices()
    # print("len ind: ", len(ind))
    # print("indices: ", ind)
    # voltage = voltage[:mesh.n_points]


    data = {'vertices': vertices, 'faces': faces, 'voltages': voltage}

    with open('xuyong_sample.json', 'w') as f:
        json.dump(data, f)

    plotter = draw_map(
        mesh=mesh,
        field=voltage,
    )
    plotter.show()

    # target_reduction = 0.1
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


    # voltage = voltage[:decimated_mesh.n_points]
    # plotter = draw_map(
    #     mesh=decimated_mesh,
    #     field=decimated_voltage,
    # )
    # plotter.show()

if __name__ == "__main__":
    main()  

