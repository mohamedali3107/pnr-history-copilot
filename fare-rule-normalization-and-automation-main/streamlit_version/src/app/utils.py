import streamlit as st

amadeus_logo = (
    "https://www.esecad.com/wp-content/uploads/sites/" "38/2018/01/Amadeus-logo.jpg"
)


def enable_chat_history(func):
    # to show chat history on ui
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": """Hello, I am Amadeus Assistant. Fill the
            flight informations and I will give you a summary of
            the fare rules !""",
            }
        ]

    for msg in st.session_state["messages"]:
        if msg["role"] == "assistant":
            with st.chat_message("assistant", avatar=amadeus_logo):
                st.write(msg["content"])
        else:
            with st.chat_message("user"):
                st.write(msg["content"])

    def execute(*args, **kwargs):
        func(*args, **kwargs)

    return execute


def display_msg(msg, author):
    """Method to display message on the UI

    Args:
        msg (str): message to display
        author (str): author of the message -user/assistant
    """
    st.session_state.messages.append({"role": author, "content": msg})
    if author == "user":
        st.chat_message(author).write(msg)
    else:
        st.chat_message(author, avatar=amadeus_logo).write(msg)
