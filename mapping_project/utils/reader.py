import os
import numpy as np
import scipy
import pyvista
import matplotlib.cm
from surface import extract_surface_data, empty_fields
from electric import extract_electric_data, empty_electric
from ablation import extract_ablation_data, empty_ablation


def _decode_tags(arr):
    """
    Convert empty arrays into empty strings. Leave strings unchanged.
    """
    return np.asarray(
        [
            item if isinstance(item, str) else item.tobytes().decode("utf-16")
            for item in arr
        ]
    )


def _cast_to_float(arr):
    """
    Cast a numpy array to float.
    """
    return [a.astype(float) if isinstance(a, np.ndarray) else a for a in arr]


def _load_mat_below_v73(filename):
    """
    Load a MATLAB file of version less than v7.3
    scipy.io.loadmat is used to read the file.
    """
    data = scipy.io.loadmat(
        filename,
        appendmat=False,
        mat_dtype=False,
        chars_as_strings=True,
        struct_as_record=False,
        squeeze_me=True,
        simplify_cells=True,
    )["userdata"]

    data["electric"]["tags"] = _decode_tags(data["electric"]["tags"])

    data["electric"]["impedances"]["time"] = _cast_to_float(
        data["electric"]["impedances"]["time"]
    )
    data["electric"]["impedances"]["value"] = _cast_to_float(
        data["electric"]["impedances"]["value"]
    )

    try:
        # this will only exist if triRep is a struct, not TriRep or Triangulation object
        data["surface"]["triRep"]["Triangulation"]

    except ValueError as e:

        if str(e) != "no field of name Triangulation":
            raise e
        else:
            message = "MATLAB classes cannot be read"
            raise TypeError(message) from e

    # rfindex is a matlab class - not readable with Python
    data.pop("rfindex", None)

    return data


def _load_mat(filename):
    """Load a MATLAB file."""
    data = _load_mat_below_v73(filename)
    # These are indices
    data["surface"]["triRep"]["Triangulation"] -= 1

    return data


def load_dataset_mat(filename, name=None):
    """
    Load the dataset from a MATLAB file.
    Args:
        filename (str): path to MATLAB file to be loaded
        name (str): name to give this dataset. The default is `None`
    Returns:
        points: the 3D vertices
        indices: the indices for the triangles
        fields: contains bi-voltage values
    """
    data = _load_mat(filename)

    if name is None:
        name = os.path.basename(filename)

    surface = extract_surface_data(data["surface"])
    electric = extract_electric_data(data["electric"])
    # ablation = extract_ablation_data(data["rf"]) if "rf" in data else None

    return surface, electric


def create_mesh(points, indices):
    """
    Function for creating the mesh

    Args:
        points (np.ndarray): array of the 3D vertices
        indices (np.ndarray): array of the indices of the faces
    """
    # indices = self.indices  # (16942, 3) faces with vertices index
    num_points_per_face = np.full(
        shape=(len(indices)), fill_value=3, dtype=int
    )  # all faces have three vertices
    faces = np.concatenate(
        [num_points_per_face[:, np.newaxis], indices], axis=1
    )  # faces with number of vertices
    arr_points = np.array(points)
    arr_meshes = faces

    # mesh = pyvista.PolyData(self.points.copy(), faces.ravel())
    mesh = pyvista.PolyData(arr_points, arr_meshes.ravel())
    # mesh = pyvista.PolyData(self.points.copy())
    return mesh


def draw_map(mesh, **kwargs):
    """
    Function for drawing the map

    Args:
        mesh: the mesh for 3D reconstruction
        field: the bi-voltage values contained
    """
    plotter = pyvista.Plotter()
    # Create default settings for the plot scalar
    default_scalar_bar_args = dict(
        interactive=False,
        color="#363737",  # set the colour of the text
        title_font_size=12,
        label_font_size=11,
        n_labels=2,
        below_label=" ",
        above_label=" ",
        vertical=False,
        width=0.3,
        height=0.05,
        position_x=0.025,
    )

    default_add_mesh_kws = {
        "style": "surface",
        "show_edges": False,
        # "smooth_shading": True,
        "annotations": False,
        "cmap": matplotlib.cm.jet_r,
        # "cmap": ['green', 'red'],
        "clim": (30, 120),
        "above_color": "magenta",
        "below_color": "brown",
        "nan_color": "gray",
        "name": "mesh",
        "opacity": 1.0,
    }

    if "field_type" in kwargs:
        field_type = kwargs.get("field_type")
        if field_type == "voltage":
            default_add_mesh_kws = {
                "style": "surface",
                "show_edges": False,
                # "smooth_shading": True,
                "annotations": False,
                "cmap": matplotlib.cm.jet_r,
                # "cmap": ['green', 'red'],
                "clim": (0, 2),
                "above_color": "magenta",
                "below_color": "brown",
                "nan_color": "gray",
                "name": "mesh",
                "opacity": 1.0,
            }
        else:
            default_add_mesh_kws = {
                "style": "surface",
                "show_edges": False,
                # "smooth_shading": True,
                "annotations": False,
                "cmap": matplotlib.cm.jet_r,
                # "cmap": ['green', 'red'],
                "clim": (30, 120),
                "above_color": "magenta",
                "below_color": "brown",
                "nan_color": "gray",
                "name": "mesh",
                "opacity": 1.0,
            }

    default_add_mesh_kws["scalar_bar_args"] = default_scalar_bar_args

    if "field" in kwargs:
        field = kwargs.get("field")
        plotter.add_mesh(
            mesh=mesh,
            scalars=field,
            **default_add_mesh_kws,
        )
    else:
        plotter.add_mesh(
            mesh=mesh,
            **default_add_mesh_kws,
        )
    # plotter.smooth()
    return plotter
