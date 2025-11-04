import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Chatgpt Clone ", page_icon=" ", layout="wide")

if "token" not in st.session_state:
    st.session_state.token = None

if "user_id" not in st.session_state:
    st.session_state.user_id = None

st.title("Chatgpt Clone -Streamlit UI")

st.subheader(" User Authentication")

option = st.radio("Choose an option", ["Login", "Register"])


email = st.text_input("Email")
password = st.text_input("Password", type="password")

if option == "Register":
    if st.button("Register"):
        res = requests.post(f"{API_BASE_URL}/auth/register",
                            json={"email": email, "password": password})
        if res.status_code == 200:
            st.success("User registered Successfully !!!!")
        else:
            st.error(f"Error {res.text}")

if option == "Login":
    if st.button("Login"):
        res = requests.post(f"{API_BASE_URL}/auth/login",
                            json={"email": email, "password": password})

        if res.status_code == 200:
            data = res.json()
            st.session_state.token = data["access_token"]
            st.session_state.user_id = data.get("user_id")
            st.success("Login Successful !! ")
        else:
            st.error("Invalid credientials")

# if st.session_state.token:
#     st.divider()
#     st.subheader("Chat with AI")

#     user_input = st.text_input("Your message:")

#     if st.button("Send"):
#         headers = {"Authorization": f"Bearer {st.session_state.token}"}
#         payload = {"message": user_input}

#         res = requests.post(
#             f"{API_BASE_URL}/chat/send_message",
#             json={"message": user_input},
#             headers=headers
#         )

#         if res.status_code == 200:
#             ai_reply = res.json().get("ai_response", "No response from AI")
#             st.chat_message("user").write(user_input)
#             st.chat_message("assistant").write(ai_reply)
#         else:
#             st.error(f"❌ {res.text}")

if st.session_state.token:
    st.divider()
    st.subheader("Chat with AI")

    # Initialize chat history if missing
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display previous messages
    for sender, msg in st.session_state.chat_history:
        st.chat_message(sender).write(msg)

    # Chat input form (so user can keep typing)
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Your message:", key="user_message_input")
        send_button = st.form_submit_button("Send")

    if send_button and user_input.strip():
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        payload = {"message": user_input}

        res = requests.post(
            f"{API_BASE_URL}/chat/send_message",
            json=payload,
            headers=headers
        )

        if res.status_code == 200:
            ai_reply = res.json().get("ai_response", "No response from AI")

            st.session_state.chat_history.append(("user", user_input))
            st.session_state.chat_history.append(("assistant", ai_reply))
            st.rerun()  # refresh to show new chat
        else:
            st.error(f"❌ {res.text}")
