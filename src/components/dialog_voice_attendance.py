import streamlit as st
from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.config import supabase
from datetime import datetime

from src.components.dialog_attendance_result import show_attendance_result
import pandas as pd


@st.dialog("Voice Attendance")
def voice_attendance_dialog(Selected_Subject_id):
    st.write("Record the audio of students saying I AM PRESENT, then AI will recognize the students. Students should speak one at a time.")

    audio_data = st.audio_input("Record classroom audio")

    if st.button("Analyse Audio", width="stretch", type="primary"):
        if audio_data is None:
            st.warning("Please record the classroom audio first")
            return

        with st.spinner("Processing audio data"):
            enrolled_res = supabase.table('subject_students').select('*, students(*)').eq('subject_id', Selected_Subject_id).execute()
            enrolled_students = enrolled_res.data

            if not enrolled_students:
                st.warning("No students are enrolled in this course")
                return

            candidate_dict = {
                s['students']['student_id']: s['students']['voice_embeddings']
                for s in enrolled_students if s['students'].get('voice_embeddings')
            }

            if not candidate_dict:
                st.error("No enrolled students have a voice profile registered")
                return

            audio_bytes = audio_data.read()

            detected_scores = process_bulk_audio(audio_bytes, candidate_dict)

            results, attendence_to_log = [], []

            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            for node in enrolled_students:
                student = node['students']
                score = detected_scores.get(student['student_id'])
                is_present = score is not None

                results.append({
                    "name": student['name'],
                    "ID": student['student_id'],
                    "score": f"{float(score):.2f}" if is_present else "-",
                    "status": "Present" if is_present else "Absent"
                })

                attendence_to_log.append({
                    "student_id": student['student_id'],
                    "subject_id": Selected_Subject_id,
                    "timestamp": current_timestamp,
                    "is_present": bool(is_present)
                })
            st.session_state.voice_attendance_results = (Selected_Subject_id, pd.DataFrame(results), attendence_to_log)

    saved = st.session_state.get('voice_attendance_results')
    # only show results that belong to the subject currently selected
    if saved and saved[0] == Selected_Subject_id:
        st.divider()
        _, df_results, logs = saved
        show_attendance_result(df_results, logs)
