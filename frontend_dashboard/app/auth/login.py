import yaml
import streamlit as st
import streamlit_authenticator as stauth

from config import Config


st.set_page_config(
    page_title="Log in",
    page_icon=":material/login:",
    layout="centered",
    initial_sidebar_state="expanded",
)
st.title(":material/login: Log In")

with open(Config.PATH_CONFIG_YAML) as file:
    config = yaml.load(file, Loader=yaml.loader.SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

try:
    authenticator.login()
    if st.session_state["authentication_status"]:
        st.rerun()
    elif st.session_state["authentication_status"] is False:
        st.error("Username/password is incorrect")
    elif st.session_state["authentication_status"] is None:
        st.warning("Please enter your username and password")
except Exception as e:
    st.error(e)
