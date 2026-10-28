import streamlit as st
from src.ui.base_layout import style_base_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
import time
from src.pipelines.face_pipeline import predict_attendence, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject

from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card
from src.components.dialog_auto_enroll import auto_enroll_dialog


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"""Welcome, {student_data['name']}""")
        if st.button("Logout", type="secondary", key="loginbackbtn", shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data
            st.rerun()
    
    st.space()
    st.space()

    join_code = (st.query_params.get("join-code") or "").strip()
    if join_code and st.session_state.get("handled_join_code") != join_code:
        st.session_state.handled_join_code = join_code
        auto_enroll_dialog(join_code)

    c1, c2 = st.columns(2)
    with c1:
        st.header("Your enrollled Subjects")

    with c2:
        if st.button("Enroll in subject", type="primary", width="stretch"):
            enroll_dialog()

    st.divider()

    with st.spinner("Loading your enrolled subjects.."):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

        stats_map ={}

        for log in logs:
            sid = log ['subject_id']

            if sid not in stats_map:
                stats_map [sid] = {"total": 0, "attended": 0}

            stats_map [sid] ['total'] +=1

            if log.get('is_present'):
                stats_map [sid] ['attended'] += 1

        cols = st.columns(2)
        for i, sub_node in enumerate (subjects):
            sub = sub_node ['subjects']
            sid = sub['subject_id']

            stats = stats_map.get(sid,{"total": 0, "attended": 0})

            def unenroll_button():
                if st.button("Unenroll fronm this course", type="tertiary", width="stretch", icon=":material/delete_forever:", key=f"unenroll_{sid}"):
                    unenroll_student_to_subject(student_id, sid)
                    st.toast(f"unenrolled from {sub['name']} successfully")
                    st.rerun()


            with cols [i % 2]:
                subject_card(
                    name = sub ['name'],
                    code = sub['subject_code'],
                    section = sub ['section'],
                    stats =[
                        ('📅','Total', stats ['total']),
                        ('✅','Attended', stats ['attended']),
                    ],
                    footer_callback = unenroll_button
                )

    footer_dashboard()










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
    img = None
    if photo_source:
        img = np.array(Image.open(photo_source).convert("RGB"))

        with st.spinner("Verifying your identity..."):
            detected, all_ids, num_faces = predict_attendence(img)

        if num_faces == 0:
            st.warning("face not found!")
        elif num_faces > 1:
            st.warning("Multiple faces detected!")
        elif detected:
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

            audio_data = st.audio_input("record a short phrase like , I am present and my name is red john")

            if st.button("Create Account", type="primary"):
                if not new_name.strip():
                    st.warning("please enter your name")
                else:
                    with st.spinner("Creating Profile..."):
                        encodings = get_face_embeddings(img)
                        if not encodings:
                            st.error("couldn't capture your facial features for registration")
                        else:
                            face_emb = encodings[0].tolist()

                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())

                            response_data = create_student(new_name.strip(), face_embeddings=face_emb, voice_embeddings=voice_emb)

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f"Profile Created, Hi {new_name}!")
                                time.sleep(1)
                                st.rerun()

    footer_dashboard()
