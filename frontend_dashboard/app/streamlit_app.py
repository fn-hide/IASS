import streamlit as st
import plotly.io as pio

from config import Config


# Set default template to 'plotly_dark'
pio.templates.default = "plotly_dark"

# setup pages
welcome = st.Page(
    Config.PATH_WELCOME,
    title="Welcome",
    icon=":material/home:",
    default=True,
)
crop = st.Page(
    Config.PATH_CROP,
    title="Crop",
    icon=":material/draw:",
)
login = st.Page(
    Config.PATH_LOGIN,
    title="Login",
    icon=":material/login:",
)
logout = st.Page(
    Config.PATH_LOGOUT,
    title="Logout",
    icon=":material/logout:",
)

# entrypoint
if Config.MODE == "dev":
    pg = st.navigation(
        {
            "Home": [welcome, crop, logout],
        }
    )
else:
    if st.session_state.get("authentication_status", None):
        if "developer" in st.session_state["roles"]:
            pg = st.navigation(
                {
                    "Home": [welcome, logout],
                }
            )
        elif "spectator" in st.session_state["roles"]:
            pg = st.navigation(
                {
                    "Home": [welcome, logout],
                }
            )
        else:
            pg = st.navigation(
                {
                    "Home": [welcome, logout],
                }
            )
    else:
        pg = st.navigation([login])

pg.run()
