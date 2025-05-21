import streamlit as st


st.set_page_config(
    page_title="Welcome",
    page_icon=":material/login:",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title(":material/waving_hand: Welcome")

container = st.container(border=True)
container.write("Provides scraped data for demo and further development.")
