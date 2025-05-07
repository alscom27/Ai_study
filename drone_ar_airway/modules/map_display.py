import pydeck as pdk


def create_path_layer(path_data):
    return pdk.Layer(
        "LineLayer",
        data=path_data,
        get_source_position="['from_x', 'from_y']",
        get_target_position="['to_x', 'to_y']",
        get_color="[255, 0, 0]",
        get_width=5,
    )
