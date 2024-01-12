import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Amadeus Co-Pilot", page_icon=":plane:")
st.title("Amadeus Co-Pilot")

pnr_history = st.file_uploader(label="Load the PNR history", type=['txt'])

if pnr_history is not None: 
    contenu = pnr_history.read()
    st.text("Affichage du PNR History :")
    st.text(contenu)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

if "messages" not in st.session_state:
    st.session_state.messages = []
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
if prompt:=st.chat_input("What's up ?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content":prompt})
    with st.chat_message("assistant"):
        message_placeholder= st.empty()
        full_response= ""
        for response in client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        stream=True):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    

    
