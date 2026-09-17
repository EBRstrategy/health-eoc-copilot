import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="Agent Copilot",
    page_icon="🤖",
    layout="centered"
)

st.title("🛡️ Health Insurance Agent Copilot")
st.caption("Ask questions about carrier EOC documents, coverage details, and copays instantly.")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input from the chat box at the bottom
if prompt := st.chat_input("What is the primary care copay?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send query to your Make.com Webhook backend
    with st.chat_message("assistant"):
        with st.spinner("Searching EOC database..."):
            try:
                # REPLACE THE TEXT BELOW WITH YOUR ACTUAL MAKE WEBHOOK URL
                webhook_url = "https://hook.us2.make.com/ofhh5f91ta14ruundtfytgp4mwd3tw7u"
                
               response = requests.post(webhook_url, json={"query": prompt})
                
                if response.status_code in [200, 202]:
                    answer = response.content.decode('utf-8')
                else:
                    answer = f"Error: Received status code {response.status_code} from backend."
            except Exception as e:
                answer = f"Connection error: Could not reach the Make webhook. Details: {e}"
            
            st.markdown(answer)
            
    st.session_state.messages.append({"role": "assistant", "content": answer})
