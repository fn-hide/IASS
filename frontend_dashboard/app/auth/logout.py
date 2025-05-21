import yaml
import streamlit as st
import streamlit_authenticator as stauth

from config import Config


st.set_page_config(
    page_title="Log out",
    page_icon=":material/logout:",
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.title(":material/logout: Log Out")

with open(Config.PATH_CONFIG_YAML) as file:
    config = yaml.load(file, Loader=yaml.loader.SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

authenticator.logout()
st.rerun()
