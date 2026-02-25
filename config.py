#Code for configuring the bot
import re
import random

USER_ID = "user"
MODEL = "4o-mini"

COURSE_RAG_THRESHOLD = 0.2
COURSE_RAG_K = 5
MEM_RAG_THRESHOLD = 0.2
MEM_RAG_K = 5


def normalize_course_id(text: str) -> str:
    t = (text or "").strip().lower()
    t = re.sub(r"[^a-z0-9]+", "", t)
    return t or "course"


def memory_session_for_user(user_id: str) -> str:
    return f"mem_{user_id}"


def course_session_for_course(course_id: str) -> str:
    return f"course_{course_id}"


def chat_session_for(user_id: str, course_id: str) -> str:
    return f"chat_{normalize_course_id(user_id)}_{course_id}"

def save_user(username: str, user_id: str):
    with open("users.txt", 'a') as file:
        file.write(username + "," + user_id + "\n")

#Logs the user into their account
def login():
    previous_user = False
    username = input("Username: ")
    with open("users.txt", "r") as file:
        for line in file.readlines():
            user, user_id = line.split(",")
            if username == user:
                memory_session = memory_session_for_user(user_id)
                previous_user = True
        if not previous_user:
            user_id = "USER" + str(random.randint(0, 10000))
            memory_session = memory_session_for_user(user_id)
            save_user(username, user_id)
    return memory_session, user_id, previous_user