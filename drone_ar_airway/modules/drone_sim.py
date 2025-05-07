import streamlit as st
import pydeck as pdk
import time


def simulate_drone_fpv(
    start_lat, start_lon, end_lat, end_lon, altitude, speed, path_data
):
    fpv_placeholder = st.empty()

    fpv_view_state = pdk.ViewState(
        latitude=start_lat,
        longitude=start_lon,
        zoom=17,
        pitch=80,
        bearing=0,
    )

    steps = 50
    latitudes = [start_lat + (end_lat - start_lat) * i / steps for i in range(steps)]
    longitudes = [start_lon + (end_lon - start_lon) * i / steps for i in range(steps)]

    for lat, lon in zip(latitudes, longitudes):
        fpv_view_state.latitude = lat
        fpv_view_state.longitude = lon

        fpv_layer = pdk.Layer(
            "LineLayer",
            data=path_data,
            get_source_position="['from_x', 'from_y']",
            get_target_position="['to_x', 'to_y']",
            get_color="[255, 0, 0]",
            get_width=5,
        )

        ar_marker_layer = pdk.Layer(
            "TextLayer",
            data=[{"coordinates": [lon, lat], "text": "AR 공중도로"}],
            get_position="coordinates",
            get_text="text",
            get_size=20,
            get_color=[0, 255, 0],
            get_angle=0,
        )

        fpv_placeholder.pydeck_chart(
            pdk.Deck(
                layers=[fpv_layer, ar_marker_layer],
                initial_view_state=fpv_view_state,
            )
        )
        time.sleep(1.0 / speed)
