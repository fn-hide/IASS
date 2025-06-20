import streamlit as st
import pandas as pd
from PIL import Image
from streamlit_drawable_canvas import st_canvas


st.set_page_config(
    page_title="Crop",
    page_icon=":material/draw:",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title(":material/draw: Crop")

container = st.container(border=True)
container.write("Provides scraped data for demo and further development.")


def convert_line_to_opencv(x1, y1, x2, y2, left, top, width, height):
    x1_cv = x1 + left - width / 2
    y1_cv = y1 + top - height / 2
    x2_cv = x2 + left - width / 2
    y2_cv = y2 + top - height / 2
    return (int(x1_cv), int(y1_cv)), (int(x2_cv), int(y2_cv))


drawing_mode = st.sidebar.selectbox(
    "Drawing tool:",
    ("line", "polygon", "transform"),
)
stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
if drawing_mode == "point":
    point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)
stroke_color = st.sidebar.color_picker("Stroke color hex: ")
bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])
if bg_image:
    bg_image = Image.open(bg_image)
realtime_update = st.sidebar.checkbox("Update in realtime", True)

# Create a canvas component
if bg_image:
    height = bg_image._size[1]
    width = bg_image._size[0]
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_image=bg_image if bg_image else None,
        update_streamlit=realtime_update,
        height=height,
        width=width,
        drawing_mode=drawing_mode,
        point_display_radius=point_display_radius if drawing_mode == "point" else 0,
        display_toolbar=st.sidebar.checkbox("Display toolbar", True),
        key="full_app",
    )

    # Do something interesting with the image data and paths
    # if canvas_result.image_data is not None:
    #     st.image(canvas_result.image_data)

    if canvas_result.json_data is not None:
        data = canvas_result.json_data["objects"]
        objects = pd.json_normalize(data)
        for col in objects.select_dtypes(include=["object"]).columns:
            objects[col] = objects[col].astype("str")
        st.dataframe(objects)

        data = [[item[1], item[2]] for item in data[0].get("path") if len(item) == 3]
        print(data)
