import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st
from src.database.db import get_all_students


@st.cache_resource
def load_dlib_mdodels():

    detactor = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detactor, sp, facerec


def get_face_embeddings(image_np):

    detactor, sp, facerec = load_dlib_mdodels()
    faces = detactor(image_np, 1)

    encodings = []

    for face in faces:

        shape = sp(image_np, face)

        face_descriptor = facerec.compute_face_descriptor(
            image_np,
            shape,
            1
        )

        encodings.append(np.array(face_descriptor))

    return encodings


@st.cache_resource
def get_trained_model():

    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:

        embeddings = student.get("face_embeddings")
        student_id = student.get("student_id")

        if embeddings:

            X.append(
                np.array(embeddings)
            )

            y.append(student_id)

    if len(X) == 0:
        return None

    all_students = sorted(list(set(y)))

    # SVC cannot train with only one student
    if len(all_students) < 2:
        return {
            "clf": None,
            "X": X,
            "y": y
        }

    clf = SVC(
        kernel="linear",
        probability=True,
        class_weight="balanced"
    )

    clf.fit(X, y)

    return {
        "clf": clf,
        "X": X,
        "y": y
    }


def train_classifier():

    st.cache_resource.clear()

    model_data = get_trained_model()

    return bool(model_data)


def predict_attendence(class_image_np):

    encodings = get_face_embeddings(class_image_np)

    detected_student = {}

    model_data = get_trained_model()

    if not model_data:
        return detected_student, [], len(encodings)

    clf = model_data["clf"]
    X_train = model_data["X"]
    y_train = model_data["y"]

    all_students = sorted(list(set(y_train)))

    for encoding in encodings:

        if clf is not None:

            predicted_id = int(
                clf.predict([encoding])[0]
            )

            student_embedding = X_train[
                y_train.index(predicted_id)
            ]

        else:

            best_distance = float("inf")
            predicted_id = None
            student_embedding = None

            for i, train_embedding in enumerate(X_train):

                distance = np.linalg.norm(
                    train_embedding - encoding
                )

                if distance < best_distance:

                    best_distance = distance
                    predicted_id = y_train[i]
                    student_embedding = train_embedding

            if predicted_id is None:
                continue

        best_match_score = np.linalg.norm(
            student_embedding - encoding
        )

        reseamblence_threshold = 0.6

        if best_match_score <= reseamblence_threshold:

            detected_student[predicted_id] = True

    return detected_student, all_students, len(encodings)