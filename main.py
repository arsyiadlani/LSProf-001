import streamlit as st
import requests

API_URL_RAG = "https://arsyiadlani-lsprof-ai.hf.space/api/v1/prediction/68732f88-b36c-4e3e-b6f6-6100b6f0311b"
API_URL_SMALL_TALK_CLASSIFIER = "https://arsyiadlani-lsprof-ai.hf.space/api/v1/prediction/a2797206-372e-493b-9717-c43c272d3053"
API_URL_SMALL_TALK_CHATBOT = "https://arsyiadlani-lsprof-ai.hf.space/api/v1/prediction/1359f923-1a9e-4b87-9300-36b79a6837bc"
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

st.title("Ask Anything about LSP Astra with LSProf!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(name=message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input():
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Check whether small talk or not
    small_talk_or_not = query_small_talk_classifier({"question": prompt})['text']
    if small_talk_or_not == "Yes":
        response = query_small_talk_chatbot({"question": prompt})
        with st.chat_message("assistant"):
            st.markdown(f"**Answer:** {response['text']}")
        st.session_state.messages.append({"role": "assistant", "content": response["text"]})
    else:
        response = query_rag({"question": prompt})
        with st.chat_message("assistant"):
            st.markdown(f"**Answer:** {response['text']}")
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
