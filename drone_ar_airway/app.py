import streamlit as st
import pydeck as pdk
import time
from geopy.geocoders import Nominatim

st.set_page_config(layout="wide")


# 주소를 좌표로 변환
@st.cache_data
def get_coordinates(address):
    geolocator = Nominatim(user_agent="drone_ar_sim")
    location = geolocator.geocode(address)
    if location:
        return location.longitude, location.latitude
    return None, None


st.title("🛰️ 드론 공중도로 AR 시야 시뮬레이터")

start_address = st.text_input("출발지 주소", "광화문")
end_address = st.text_input("도착지 주소", "서울역")

start_coords = get_coordinates(start_address)
end_coords = get_coordinates(end_address)

if start_coords and end_coords:
    start_lon, start_lat = start_coords
    end_lon, end_lat = end_coords
    st.success(
        f"✅ 출발지: {start_address} → 좌표: {start_coords}\n✅ 도착지: {end_address} → 좌표: {end_coords}"
    )
else:
    st.error(
        "❗ 출발지 또는 도착지 주소를 찾을 수 없습니다. 정확한 주소를 입력해주세요."
    )
    st.stop()

# 시뮬레이션 설정
altitude = st.slider("고도 (m)", 10, 100, 30)
speed = st.slider("드론 속도 (1=느림, 10=빠름)", 1, 10, 3)

path_data = [
    {
        "id": "route",
        "from_x": start_lon,
        "from_y": start_lat,
        "from_z": altitude,
        "to_x": end_lon,
        "to_y": end_lat,
        "to_z": altitude,
    }
]

# 지도에 경로 표시
path_layer = pdk.Layer(
    "LineLayer",
    data=path_data,
    get_source_position="['from_x', 'from_y']",
    get_target_position="['to_x', 'to_y']",
    get_color="[255, 0, 0]",
    get_width=5,
)

view_state = pdk.ViewState(
    latitude=(start_lat + end_lat) / 2,
    longitude=(start_lon + end_lon) / 2,
    zoom=14,
    pitch=45,
)

st.pydeck_chart(pdk.Deck(layers=[path_layer], initial_view_state=view_state))

# 🛰️ 드론 시뮬레이션 애니메이션
if st.button("🚀 드론 시뮬레이션 시작"):
    placeholder = st.empty()
    steps = 50
    latitudes = [start_lat + (end_lat - start_lat) * i / steps for i in range(steps)]
    longitudes = [start_lon + (end_lon - start_lon) * i / steps for i in range(steps)]

    for lat, lon in zip(latitudes, longitudes):
        drone_layer = pdk.Layer(
            "ScatterplotLayer",
            data=[{"lon": lon, "lat": lat}],
            get_position="[lon, lat]",
            get_color="[0, 200, 255]",
            get_radius=15,
        )
        placeholder.pydeck_chart(
            pdk.Deck(layers=[path_layer, drone_layer], initial_view_state=view_state)
        )
        time.sleep(1.0 / speed)

# 🎥 드론 시야(FPV) + 3D 공중도로 + AR 표식
if st.button("🎥 드론 시야(FPV) + AR 보기"):
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
    altitudes = [altitude for _ in range(steps)]

    for lat, lon, alt in zip(latitudes, longitudes, altitudes):
        fpv_view_state.latitude = lat
        fpv_view_state.longitude = lon

        fpv_layer = pdk.Layer(
            "PathLayer",
            data=[
                {
                    "path": [
                        [start_lon, start_lat, altitude],
                        [end_lon, end_lat, altitude],
                    ]
                }
            ],
            get_path="path",
            get_color="[255, 100, 100]",
            width_scale=10,
            width_min_pixels=5,
            rounded=True,
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
                map_style="mapbox://styles/mapbox/dark-v11",
                parameters={"depthTest": True},
            )
        )
        time.sleep(1.0 / speed)
