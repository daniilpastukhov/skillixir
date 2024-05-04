import wikipedia
from enum import IntEnum
from tempfile import NamedTemporaryFile

from openai import OpenAI
import streamlit as st
from streamlit_searchbox import st_searchbox


class Step(IntEnum):
    UPLOAD_RESUME = 1
    CHOOSE_POSITIONS = 2
    CHAT = 3


def handle_pdf_upload(files):
    pass

def handle_position_selection(positions):
    pass

def handle_chat(chat_message):
    pass

def search_wikipedia(searchterm: str) -> list[any]:
    return wikipedia.search(searchterm) if searchterm else []

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

st.title("🧙‍♂️ Skilixir")
st.caption("Analyze your resume against current market openings.")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello, please upload your resume to get started."}]
    st.session_state['step'] = Step.UPLOAD_RESUME

print('running +', st.session_state['step'])
print(st.session_state['step'] == Step.UPLOAD_RESUME)
if st.session_state['step'] == Step.UPLOAD_RESUME:
    uploaded_fileis = st.file_uploader("Upload your resume in .pdf format", accept_multiple_files=False)
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        with NamedTemporaryFile(suffix='pdf') as temp_file:
            temp_file.write(bytes_data)
            temp_file.seek(0)
            print(temp_file.name)
            st.session_state['uploaded_file'] = temp_file.name
            st.session_state.messages.append({"role": "assistant", "content": 'Great, now choose the positions you are interested in.'})
        st.session_state['step'] = Step.CHOOSE_POSITIONS
        st.rerun()
    
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if st.session_state['step'] == Step.CHOOSE_POSITIONS:
    option = st.selectbox(
        'How would you like to be contacted?',
        ('Email', 'Home phone', 'Mobile phone'))

    st.write('You selected:', option)

if prompt := st.chat_input():
    print('INPUT')
    # if not openai_api_key:
    #     st.info("Please add your OpenAI API key to continue.")
    #     st.stop()
    print(st.session_state['step'])
    print(st.session_state['step'] == Step.UPLOAD_RESUME)
    if st.session_state['step'] == Step.CHOOSE_POSITIONS:
        st.session_state['step'] = Step.CHAT
        
        # st.session_state.messages.append({"role": "user", "content": prompt})
        # st.session_state.messages.append({"role": "assistant", "content": "Let's chat about your resume and the selected positions."})
        # st.chat_message("user").write(prompt)
        # st.chat_message("assistant").write("Let's chat about your resume and the selected positions.")
    elif st.session_state['step'] == Step.CHAT:
        # st.session_state.messages.append({"role": "user", "content": prompt})
        # st.chat_message("user").write(prompt)
        # client = OpenAI(api_key=openai_api_key)
        pass
    else:
        # st.session_state.messages.append({"role": "user", "content": prompt})
        # st.chat_message("user").write(prompt)
        # client = OpenAI(api_key=openai_api_key)
        # response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        # msg = response.choices[0].message.content
        # st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write('Please upload your resume first.')
        
    
