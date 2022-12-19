
import numpy as np
import pandas as pd
import pyvista
from case import interpolators
from reader import load_dataset_mat, create_mesh, draw_map

## Read the dataset
filename = "./data/dataset_1.mat"
points, indices, fields, electric = load_dataset_mat(filename)

## Creating map with the Carto calculated vol/lat info
# Createing mesh
mesh = create_mesh(points, indices)
vertices = mesh.points
faces = mesh.faces

# Get the vol/lat info
voltage = fields.bipolar_voltage
lat = fields.local_activation_time
# df = pd.DataFrame(voltage)
# print(df.describe())
# print("Carto calculated voltage: ", voltage)

# Display the map with Carto calculation
mesh = pyvista.PolyData(vertices, faces)

# plotter = draw_map(
#     mesh=mesh,
#     field=voltage,
# )
# plotter.show()

# Interpolation algo
interpolator_voltage = interpolators.LocalSMoothingInterpolator(
    points=electric.bipolar_egm.points,
    field=electric.bipolar_egm.voltage,
)
interpolated_voltage = interpolator_voltage(new_points=points)

# Interpolation algo
lat = electric.annotations.local_activation_time - electric.annotations.reference_activation_time
interpolator_lat = interpolators.LocalSMoothingInterpolator(
    points=electric.bipolar_egm.points,
    field=lat
)
interpolated_lat = interpolator_lat(new_points=points)

# df = pd.DataFrame(interpolated_voltage)
# print(df.describe())
# print("interpolated_voltage: ", interpolated_voltage)

plotter = draw_map(
    mesh=mesh,
    field=interpolated_voltage,
)
plotter.show()
