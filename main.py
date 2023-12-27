import streamlit as st
import requests
import time

API_URL_RAG = "https://arsyiadlani-lsprofai.hf.space/api/v1/prediction/9b9e69d2-3962-415c-af92-e73a90725009"
API_URL_SMALL_TALK_CLASSIFIER = "https://arsyiadlani-lsprofai.hf.space/api/v1/prediction/9b156c26-8ff7-4756-bb55-09835c6f7660"
API_URL_SMALL_TALK_CHATBOT = "https://arsyiadlani-lsprofai.hf.space/api/v1/prediction/d9c162bd-087f-4cee-97fc-98ec9c9a6af1"
API_URL_RETRIEVAL_RELEVANCE_CLASSIFIER = "https://arsyiadlani-lsprof-ai.hf.space/api/v1/prediction/0c643785-8154-44af-9e1d-6f739fb9dbc2"

human_avatar = "🧑"
ai_avatar = "https://cdn-icons-png.flaticon.com/512/3890/3890633.png"
page_avatar_2 = "https://drive.google.com/uc?export=view&id=1M3XDekX13PmunujV-nTSgpdF400kNqmT"
lsprof_logo = "https://drive.google.com/uc?export=view&id=1hqfgurlvhem8JksCpdhBz893iZ2vFKTw"

def query_rag(payload):
    response = requests.post(API_URL_RAG, json=payload)
    print(response.json()['text'])
    return response.json()

def query_small_talk_classifier(payload):
    response = requests.post(API_URL_SMALL_TALK_CLASSIFIER, json=payload)
    print(response.json()['text'])
    return response.json()

def query_small_talk_chatbot(payload):
    response = requests.post(API_URL_SMALL_TALK_CHATBOT, json=payload)
    print(response.json()['text'])
    return response.json()

def query_retrieval_relevance_classifier(payload):
    response = requests.post(API_URL_RETRIEVAL_RELEVANCE_CLASSIFIER, json=payload)
    print(response.json()['text'])
    return response.json()

def clear_session():
    requests.delete(API_URL_RAG)
    requests.delete(API_URL_SMALL_TALK_CHATBOT)

def ask_prompt(prompt):
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
                   page_icon=page_avatar_2, 
                   layout="centered", 
                   initial_sidebar_state="auto", 
                   menu_items=None)

col1, col2, col3 = st.columns(3)
with col2:
    st.image(lsprof_logo)
    
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
    ask_prompt(prompt=prompt)
elif template_button_1:
    prompt = template_message_1
    ask_prompt(prompt=prompt)
elif template_button_2:
    prompt = template_message_2
    ask_prompt(prompt=prompt)
elif template_button_3:
    prompt = template_message_3 
    ask_prompt(prompt=prompt)
elif template_button_4:
    prompt = template_message_4
    ask_prompt(prompt=prompt)
