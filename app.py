import streamlit as st
import os
import shutil
import query_data
import create_database

def main():
    st.set_page_config(page_title="Chat With files")
    st.header("Chat with your PDF files")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "processComplete" not in st.session_state:
        st.session_state.processComplete = None

    with st.sidebar:
        uploaded_files =  st.file_uploader("Upload your file",type=['pdf'],accept_multiple_files=True)
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        process = st.button("Process")
    if process:
        if openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        os.makedirs('data/uploaded_files', exist_ok=True)

        for uploaded_file in uploaded_files:
            with open(os.path.join('data/uploaded_files', uploaded_file.name), 'wb') as f:
                f.write(uploaded_file.getbuffer())

        create_database.main()

        st.session_state.processComplete = True

    if  st.session_state.processComplete == True:
        user_question = st.chat_input("Chat with your file")
        if user_question:
            result = query_data.main(user_question)
            st.text(result)

if __name__ == "__main__":
    main()