import streamlit as st
import requests
import time

API_URL_RAG = "https://arsyiadlani-lsprofai.hf.space/api/v1/prediction/9b9e69d2-3962-415c-af92-e73a90725009"
API_URL_SMALL_TALK_CLASSIFIER = "https://arsyiadlani-lsprofai.hf.space/api/v1/prediction/9b156c26-8ff7-4756-bb55-09835c6f7660"
API_URL_SMALL_TALK_CHATBOT = "https://arsyiadlani-lsprofai.hf.space/api/v1/prediction/d9c162bd-087f-4cee-97fc-98ec9c9a6af1"
API_URL_RETRIEVAL_RELEVANCE_CLASSIFIER = "https://arsyiadlani-lsprof-ai.hf.space/api/v1/prediction/0c643785-8154-44af-9e1d-6f739fb9dbc2"

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

st.set_page_config(page_title="LSProf Virtual AI Assistant", 
                   page_icon="🤖", 
                   layout="centered", 
                   initial_sidebar_state="auto", 
                   menu_items=None)

st.title("Tanya apa saja tentang LSP Astra kepada LSProf 👇🏻")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"]=="user":
        with st.chat_message(name="user", avatar="🧑"):
            st.markdown(message["content"])
    elif message["role"]=="assistant":
        with st.chat_message(name="assistant"):
            st.markdown(message["content"])

if prompt := st.chat_input("Tanya LSProf..."):
    with st.chat_message(name="user", avatar="🧑"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Check whether small talk or not
    small_talk_or_not = query_small_talk_classifier({"question": prompt})['text']
    if small_talk_or_not == "Yes":
        response = query_small_talk_chatbot({"question": prompt})
        with st.chat_message(name="assistant"):
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
        with st.chat_message(name="assistant"):
            assistant_response = response['text']
            message_placeholder = st.empty()
            full_response = ""
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.09)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": response["text"]})


    # # Check whether small talk or not
    # small_talk_or_not = query_small_talk_classifier({"question": prompt})['text']
    # if small_talk_or_not == "Yes":
    #     response = query_small_talk_chatbot({"question": prompt})
    #     with st.chat_message("assistant"):
    #         st.markdown(f"**Answer:** {response['text']}")
    #     st.session_state.messages.append({"role": "assistant", "content": response["text"]})
    # else:
    #     relevance_or_not = query_retrieval_relevance_classifier({"question": prompt})['text']
    #     if relevance_or_not == "Yes":
    #         response = query_rag({"question": prompt})
    #         with st.chat_message("assistant"):
    #             st.markdown(f"**Answer:** {response['text']}")
    #         st.session_state.messages.append({"role": "assistant", "content": response["text"]})
    #     else:
    #         response = query_small_talk_chatbot({"question": prompt})
    #         with st.chat_message("assistant"):
    #             st.markdown(f"**Answer:** {response['text']}")
    #         st.session_state.messages.append({"role": "assistant", "content": response["text"]})
    #
