import streamlit as st
from openai import OpenAI
import yaml 

st.set_page_config(page_title="Amadeus Co-Pilot", page_icon=":plane:")
st.title("Amadeus Co-Pilot")

pnr_history_file = st.file_uploader(label="Load the PNR history", type=['txt'])
pnr_history = None

if pnr_history_file is not None: 
    pnr_history = pnr_history_file.read()
    #st.text("Affichage du PNR History :")
    #st.text(contenu)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

if "messages" not in st.session_state:
    st.session_state.messages = []
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

llm_settings= yaml.load(open('ChatBotConfig.yml', 'r'), Loader=yaml.FullLoader)
if pnr_history is None:
    systemp_prompt = llm_settings["prompts"]["not-uploaded"]

if pnr_history is not None:     
    pnr_history_str= pnr_history.decode("utf-8")
    systemp_prompt = llm_settings["prompts"]["uploaded"] + pnr_history_str + llm_settings["prompts"]["pnr_meaning"]
        
if prompt:=st.chat_input("What's up ?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    prompt = prompt 
    st.session_state.messages.append({"role": "user", "content":prompt})
    with st.chat_message("assistant"):
        message_placeholder= st.empty()
        full_response= ""
        for response in client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[{"role": "user", "content": systemp_prompt}] + [{"role": m["role"], "content": prompt} for m in st.session_state.messages],
        stream=True):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    

    
