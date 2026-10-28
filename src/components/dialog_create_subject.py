import streamlit as st
from src.database.db import create_subject


@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the details of new subject")
    sub_id = st.text_input("Enter your subject code", placeholder="CS101")
    sub_name = st.text_input("subject name", placeholder="Introduction to Computer Science")
    sub_section = st.text_input("subject section", placeholder="A")


    if st.button("Create Subject Now", type="primary", width="stretch"):
        sub_id, sub_name, sub_section = sub_id.strip(), sub_name.strip(), sub_section.strip()
        if sub_id and sub_name and sub_section :
            try:
                create_subject(sub_id, sub_name, sub_section, teacher_id)
                st.toast("Subject Created Successfully")
                st.rerun()
            except Exception as e:
                st.error(f"Could not create subject (code may already exist): {e}")
        else:
            st.warning("Please fill all the fields")