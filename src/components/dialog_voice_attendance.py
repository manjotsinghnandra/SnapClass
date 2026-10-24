import streamlit as st
from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.config import supabase
from datetime import datetime

from src.components.dialog_attendance_result import show_attendance_result
import pandas as pd

@st.dialog("Voice Attendance")
def voice_attendance_dialog(Selected_Subject_id):
    st.write("Record the audio of students saying I AM PRESENT , Then ai will recognize the students")

    audio_data = None

    audio_data = st.audio_input("Record classroom audio")

    if st.button("Analyse Audio", width="stretch", type="primary"):
        with st.spinner("Procesing audio data"):
            enrolled_res = supabase.table('subject_students').select('*, students(*)').eq('subject_id', Selected_Subject_id).execute()
            enrolled_students = enrolled_res.data
            
            if not enrolled_students:
                st.warning("No students are enrolled in this course")
                return
            candidate_dict ={
                s['students']['student_id'] : s['students']['voice_embeddings']
                for s in enrolled_students if s['students'].get('voice_embeddings')
            }

            if not candidate_dict:
                st.error("NO enrolled students have voice profled registerd")
                return

            audio_bytes = audio_data.read()

            detected_scores = process_bulk_audio(audio_bytes, candidate_dict)

            results, attendence_to_log = [], []
    
            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            for node in enrolled_students:
                student = node['students']
                score = detected_scores.get(student['student_id'], 0.0)
                is_present = bool(score>0)

                results.append({
                    "name": student['name'],
                    "ID": student['student_id'],
                    "source": score if is_present else "-",
                    "status": "Present" if is_present else "Absent"
                })

                attendence_to_log.append({
                    "student_id": student['student_id'],
                    "subject_id": Selected_Subject_id,
                    "timestamp": current_timestamp,
                    "is_present": bool(is_present)
                })
            st.session_state.voice_attendance_results = (pd.DataFrame(results), attendence_to_log)

    if st.session_state.get('voice_attendance_results'):
        st.divider()
        df_results, logs = st.session_state.voice_attendance_results
        show_attendance_result(df_results, logs)