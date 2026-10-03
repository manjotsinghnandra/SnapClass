from src.database.config import supabase
import bcrypt


def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()


def check_password(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())


def check_teacher_exists(username):
    response = supabase.table("teachers").select("username").eq("username",username).execute()
    return len(response.data) > 0


def create_teacher(username, name, password):
    data = {
        "username": username,
        "password": hash_pass(password),
        "name": name,
    }
    response = supabase.table("teachers").insert(data).execute()
    return response


def teacher_login(username, password):
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if check_password(password, teacher["password"]):
            return teacher
    return None











def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data

def create_student(new_name, face_embeddings=None, voice_embeddings=None):
    data = {"name":new_name,
            "face_embeddings":face_embeddings,
            "voice_embeddings":voice_embeddings
            }
    response = supabase.table('students').insert(data).execute()
    return response.data