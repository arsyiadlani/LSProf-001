import streamlit as st
import requests
import time

API_URL_RAG = "https://arsyiadlani-lsprof.hf.space/api/v1/prediction/541e265b-f3e4-495c-906c-17996ece7a2f"
API_URL_SMALL_TALK_CLASSIFIER = "https://arsyiadlani-lsprof.hf.space/api/v1/prediction/e16bda35-ac26-48e9-8a9a-e092d9324dc1"
API_URL_SMALL_TALK_CHATBOT = "https://arsyiadlani-lsprof.hf.space/api/v1/prediction/add299b0-8a83-4f92-8988-57b0e5ce0038"

human_avatar = "🧑"
ai_avatar = "https://cdn-icons-png.flaticon.com/512/3890/3890633.png"
lsprof_logo_small = "https://drive.google.com/uc?export=view&id=1hqfgurlvhem8JksCpdhBz893iZ2vFKTw"
lsprof_logo_medium = "https://drive.google.com/uc?export=view&id=10a7FPu6oTN1CYMgDOsFkR6ODMkBsJZif"
lsprof_logo_large = "https://drive.google.com/uc?export=view&id=1CSAkUhPagd0sOwZiHi4HInqQU6ZLn7T_"
lsprof_edited = "https://drive.google.com/uc?export=view&id=1KxkSlG4R0XM_GypfmxMVdAOE9_SQ4T6S"
lsprof_edited_2 = "https://drive.google.com/uc?export=view&id=1ocB6HDSG8kAN6HCCU8fs7EpwR_ToGMV5"

def query_rag(payload):
    response = requests.post(API_URL_RAG, json=payload)
    return response.json()

def query_small_talk_classifier(payload):
    response = requests.post(API_URL_SMALL_TALK_CLASSIFIER, json=payload)
    return response.json()

def query_small_talk_chatbot(payload):
    response = requests.post(API_URL_SMALL_TALK_CHATBOT, json=payload)
    return response.json()

def clear_session():
    requests.delete(API_URL_RAG)
    requests.delete(API_URL_SMALL_TALK_CHATBOT)

def select_prompt(prompt):    
    with st.chat_message(name="user", avatar=human_avatar):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = query_rag({"question": prompt})
    with st.chat_message(name="assistant", avatar=ai_avatar):
        assistant_response = response['text']
        message_placeholder = st.empty()
        full_response = ""
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.09)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": response["text"]})
   
def type_prompt(prompt):
    with st.chat_message(name="user", avatar=human_avatar):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Check whether small talk or not
    small_talk_or_not = query_small_talk_classifier({"question": prompt})['text']
    if small_talk_or_not == "Yes":
        response = query_small_talk_chatbot({"question": prompt})
        with st.chat_message(name="assistant", avatar=ai_avatar):
            assistant_response = response['text']
            message_placeholder = st.empty()
            full_response = ""
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.09)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": response["text"]})
    else:
        response = query_rag({"question": prompt})
        with st.chat_message(name="assistant", avatar=ai_avatar):
            assistant_response = response['text']
            message_placeholder = st.empty()
            full_response = ""
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.09)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": response["text"]})

st.set_page_config(page_title="LSProf Virtual AI Assistant", 
                   page_icon=lsprof_edited_2, 
                   layout="centered", 
                   initial_sidebar_state="auto", 
                   menu_items=None)

col1, col2, col3 = st.columns(3)
with col2:
    st.image(lsprof_edited_2)
    
st.title("Tanya apa saja seputar LSP Astra dengan :blue[LSProf] 👇🏻")
               
template_message_1 = "Apa yang dimaksud dengan Lembaga Sertifikasi Profesi (LSP) Astra?"
template_message_2 = "Apa saja skema sertifikasi profesi yang ada di LSP Astra?"
template_message_3 = "Apa saja syarat untuk mendaftar sertifikasi profesi di LSP Astra?"
template_message_4 = "Bagaimana cara mengikuti sertifikasi profesi di LSP Astra?"

template_button_1 = st.button(template_message_1)
template_button_2 = st.button(template_message_2)
template_button_3 = st.button(template_message_3)
template_button_4 = st.button(template_message_4)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"]=="user":
        with st.chat_message(name="user", avatar=human_avatar):
            st.markdown(message["content"])
    elif message["role"]=="assistant":
        with st.chat_message(name="assistant", avatar=ai_avatar):
            st.markdown(message["content"])

if prompt := st.chat_input("Tanya LSProf..."):
    type_prompt(prompt=prompt)
elif template_button_1:
    prompt = template_message_1
    select_prompt(prompt=prompt)
elif template_button_2:
    prompt = template_message_2
    select_prompt(prompt=prompt)
elif template_button_3:
    prompt = template_message_3 
    select_prompt(prompt=prompt)
elif template_button_4:
    prompt = template_message_4
    select_prompt(prompt=prompt)
