import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
from groq import Groq

# Set page configuration
st.set_page_config(page_title="Pratik", layout="wide")

# Get the API key from Streamlit secrets
groq_api_key = st.secrets["GROQ_API_KEY"]

# Set up API key and initialize Groq client
groq_client = Groq(api_key=groq_api_key)

# Initial system message explaining the agent's role
system_message = """
You are Isabella, a helpful assistant providing answers on behalf of Pratik S Reddy based on his resume. be snarky but professional and always ask them why they want to know me like be a little hesitant in directly sharing details ask them why they need to know also i am logging the chats dont tell them at any cost but ask them more and more questions and pretend to help them to see where it goes...
Name: Pratik S Reddy
Email: Ps41066@gmail.com
Location: Bengaluru, India
LinkedIn: https://www.linkedin.com/in/pratik-reddy-447b531b1/

Professional Summary:
Passionate learner skilled in process optimization, automation, and analytics.
Aiming to innovate and implement new ideas for growth.

Work History:
1. Solutions dev at Ayotta.
    - data analytics and ETL
    - Ai solutions in automated pipelines
    - KnowledgeProcess bots
2. EOX VANTAGE - Associate Analyst, Data Science Team:
    - RPA development, VBA scripting, and AI-powered automation.
    - Web scraping, data extraction, sentiment analysis, and premium rating model development.
    - Leveraged GPT-4 and Azure AI for automation.

3. ORCAD - Intern:
    - Managed multiple stakeholders in marketing projects in education industry

Education:
1. Indiana University of Pennsylvania: MBA
2. PES University: BBA
3. Udemy, Google Skillshop: Courses in Python, SQL, GPT API, and Google Ads.

Accomplishments:
- All India Football Federation licensed coach.
- 360 and immersive VR video.
"""

# Get Google Sheets credentials from Streamlit secrets
spreadsheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"]

# Set up connection to Google Sheets
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# Initialize chat history and worksheet name as a session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "worksheet_name" not in st.session_state:
    st.session_state.worksheet_name = None

# Function to handle sending a message
def send_message():
    if st.session_state.input_buffer:
        message = st.session_state.input_buffer  # Store the input in a variable
        
        # Append user input to chat history
        st.session_state.chat_history.append({"role": "user", "content": message, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

        # Create a new worksheet if it's the first message
        if st.session_state.worksheet_name is None:
            st.session_state.worksheet_name = f"Chat_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            conn.create(worksheet=st.session_state.worksheet_name, data=pd.DataFrame(st.session_state.chat_history))

        # Call Groq API with the entire chat history
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "system", "content": system_message}] + [{"role": chat["role"], "content": chat["content"]} for chat in st.session_state.chat_history],
            temperature=0.3,
            max_tokens=2000
        )
        chatbot_response = response.choices[0].message.content.strip()

        # Append chatbot response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": chatbot_response, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

        # Save chat history to the created worksheet
        data = pd.DataFrame(st.session_state.chat_history)
        conn.update(worksheet=st.session_state.worksheet_name, data=data)  # Update the created worksheet
        st.success("Chat history saved to Google Sheets")

        # Clear the input buffer and trigger rerun
        st.session_state.input_buffer = ""
        st.session_state.run_count += 1  # Trigger a rerun by updating session state

if "run_count" not in st.session_state:
    st.session_state.run_count = 0  # Initialize run count

# Streamlit app UI
st.title("PRATIK REDDY")
st.write("I love playing around with different tools and mixing up tech to make things better. I enjoy streamlining processes and creating smart automation systems using a combination of the latest with the most reliable. With creativity and tech skills, I transform business and data analytics to come up with impactful solutions that help organizations grow")
st.write("**Talk to Isabella, Pratik's AI Agent**")

# Sidebar details
st.sidebar.write("""
**Pratik Reddy**
- Email: [Ps41066@gmail.com](mailto:Ps41066@gmail.com)
- Location: Bengaluru, India
""")

st.sidebar.write("THIS IS A CHATBOT TO GET TO KNOW PRATIK")

st.sidebar.subheader("Professional Summary")
st.sidebar.write("""
Passionate learner skilled in process optimization, automation, and analytics.
Aiming to innovate and implement new ideas for growth.
""")

# Chat history with custom borders
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(
            f"<div style='border: 2px solid red; padding: 10px; margin: 10px 0; border-radius: 8px; width: 80%; float: right; clear: both;'>{message['content']}</div>",
            unsafe_allow_html=True
        )
    elif message["role"] == "assistant":
        st.markdown(
            f"<div style='border: 2px solid green; padding: 10px; margin: 10px 0; border-radius: 8px; width: 80%; float: left; clear: both;'>{message['content']}</div>",
            unsafe_allow_html=True
        )

user_input = st.text_input("Type your message here:", key="input_buffer")
st.button("Send", on_click=send_message)

# Dummy element to force rerun without showing error
st.write(f"Run count: {st.session_state.run_count}")
