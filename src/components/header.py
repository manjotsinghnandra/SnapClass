import streamlit as st
from src.ui.base_layout import theme_toggle


def header_home():

    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"

    st.markdown(f"""
            <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:30px; margin-top:30px">
                <img src='{logo_url}' style='height:100px;' />
                <h1 style='text-align:center; color:var(--color-primary)'>SNAP<br/>CLASS</h1>
            </div>
                """, unsafe_allow_html=True)

    # Place toggle in the top-right of the home header
    with st.container():
        _, toggle_col = st.columns([6, 1])
        with toggle_col:
            theme_toggle()


def header_dashboard():

    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"

    st.markdown(f"""
            <div style="display:flex; align-items:center; justify-content:center; gap:10px;">
                <img src='{logo_url}' style='height:85px;' />
                <h2 style='text-align:left; color:var(--color-primary)'>SNAP<br/>CLASS</h2>
            </div>
                """, unsafe_allow_html=True)