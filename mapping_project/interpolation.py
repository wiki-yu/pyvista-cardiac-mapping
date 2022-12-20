import pyvista
import pandas as pd
from utils import interpolators
from utils.reader import load_dataset_mat, create_mesh, draw_map


def main():
    """
    The basic workflow of the interpolation
    """
    ## Read the dataset
    filename = "../data/dataset_1.mat"
    surface, electric = load_dataset_mat(filename)
    points = surface["points"]
    indices = surface["indices"]
    fields = surface["fields"]

    ## Creating map with the Carto calculated voltage/lat info
    # Createing mesh
    mesh = create_mesh(points, indices)
    # Get the vol/lat info
    voltage = fields.bipolar_voltage
    lat = fields.local_activation_time
    print("Vol data len:{}, LAT data len:{}".format(len(voltage), len(lat)))  # 9279
    # df = pd.DataFrame(voltage)
    # print(df.describe())
    # print("Carto calculated voltage: ", voltage)

    # Display the map with Carto calculation
    # mesh = pyvista.PolyData(vertices, faces)
    # plotter = draw_map(
    #     mesh=mesh,
    #     field=voltage,
    #     field_type="voltage"
    # )
    # plotter.show()

    ## Interpolation
    # Interpolation for voltage
    interpolator_voltage = interpolators.NearestInterpolator(
        points=electric.bipolar_egm.points,
        field=electric.bipolar_egm.voltage,
    )
    interpolated_voltage = interpolator_voltage(new_points=points)
    print("Interpolated voltage length: ", len(interpolated_voltage))

    # Interpolation for LAT
    lat = (
        electric.annotations.local_activation_time
        - electric.annotations.reference_activation_time
    )
    interpolator_lat = interpolators.NearestInterpolator(
        points=electric.bipolar_egm.points, field=lat
    )
    interpolated_lat = interpolator_lat(new_points=points)
    print("Interpolated LAT length: ", len(interpolated_lat))

    # df = pd.DataFrame(interpolated_voltage)
    # print(df.describe())
    # print("interpolated_voltage: ", interpolated_voltage)

    # Map visualization with the interpolated data
    plotter = draw_map(mesh=mesh, field=interpolated_voltage, field_type="voltage")
    plotter.show()


if __name__ == "__main__":
    main()
