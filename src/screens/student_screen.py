import streamlit as st
from src.ui.base_layout import style_base_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
import time
from src.pipelines.face_pipeline import predict_attendence, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student


def student_dashboard():
    st.header("DASHBOARD HERE")

def student_screen():

    style_base_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard() 
        return

    
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type="secondary", key="loginbackbtn", shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()


    st.header("Login Using face id", text_alignment="center")
    st.space()


    show_registerations = False
    photo_source = st.camera_input("position your face in the center of the frame")
    if photo_source:
        img = np.array(Image.open(photo_source))

        with st.spinner("Verifying your identity..."):
            detected, all_ids, num_faces = predict_attendence(img)

            if num_faces == 0:
                st.warning("face not found!")
            elif num_faces > 1:
                st.warning("Multiple faces detected!")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s["student_id"] == student_id), None) 


                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f"Welcome back, {student['name']}!")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info("Face not recognized. you might be a new student.")
                    show_registerations = True

    if show_registerations:
        with st.container(border=True):
            st.header("Register as a new profile")
            new_name = st.text_input("enter your name", placeholder="eg: red john")

            st.subheader("optional : voice enrollment")
            st.info("enroll yourself for voice only attendance")


            audio_data = None

            try:
                audio_data = st.audio_input("record a short phrase like , I am present and my name is red john")
            except Exception:
                st.error("audio data failed")


            st.button("Create Accnount", type="primary")
            if new_name:
                with st.spinner("Creating Profile..."):
                    img = np.array(Image.open(photo_source))
                    encodings = get_face_embeddings(img)
                    if encodings:
                        face_emb = encodings[0].tolist()

                        voice_emb = None
                        if audio_data:
                            voice_emb = get_voice_embedding(audio_data.read())


                            response_data = create_student(new_name, face_embeddings=face_emb, voice_embeddings=voice_emb)


                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f"Profile Created, Hi {new_name}!")
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error("coudnt capture your facial features for regsiteration")
            else:
                st.warning("please enter your name")

    footer_dashboard()



    