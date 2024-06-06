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
You are Whis, a helpful assistant providing answers on behalf of Pratik S Reddy based on his resume. Be snarky but professional and always ask them why they want to know me. Be a little hesitant in directly sharing details; ask them why they need to know. Also, I am logging the chats—don't tell them at any cost. Ask them more and more questions and pretend to help them to see where it goes...
Name: Pratik S Reddy
Email: Ps41066@gmail.com
Location: Bengaluru, India
LinkedIn: https://www.linkedin.com/in/pratik-reddy-447b531b1/
GitHub: https://github.com/Pratikreddy
X: https://x.com/pratikredy

Professional Summary:
Passionate learner skilled in process optimization, automation, and analytics. Aiming to innovate and implement new ideas for growth.

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
st.write("Tech enthusiast blending innovation with automation.")

# Profile picture (update the URL with the raw URL of your image from GitHub)
st.image("https://github.com/Pratikreddy/resume/blob/main/1715865738291.jpeg", width=150)

# Social media links
st.markdown("""
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Pratikreddy)
[![X](https://img.shields.io/badge/X-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://x.com/pratikredy)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/pratik-reddy-447b531b1/)
""")

st.write("**This app uses an LLM served by Groq and a RAG pipeline to retrieve data from a vector index like FAISS.**")

st.write("**Talk to Whis, Pratik's AI Agent**")

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

# Placeholder for profile picture, add your picture file
st.image("https://raw.githubusercontent.com/yourusername/yourrepository/branch/path/to/profile_picture.jpg", caption="Pratik S Reddy", width=150)

# Placeholder for project section, uncomment and add projects
"""
## Projects and Technologies

### Project 1: [Project Title](project_link)
Description of the project, technologies used, and the role played by Pratik.

### Project 2: [Project Title](project_link)
Description of the project, technologies used, and the role played by Pratik.

### Project 3: [Project Title](project_link)
Description of the project, technologies used, and the role played by Pratik.

# Button to add project details to chat
if st.button('Add Project to Chat'):
    project_info = "Detailed project info to be added to chat."
    st.session_state.chat_history.append({"role": "assistant", "content": project_info, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    data = pd.DataFrame(st.session_state.chat_history)
    conn.update(worksheet=st.session_state.worksheet_name, data=data)
"""

# Updated resume details
resume = """
Work History:
1. Solutions dev at Ayotta (Started March 2023).
    - data analytics and ETL
    - Ai solutions in automated pipelines
    - KnowledgeProcess bots
2. EOX VANTAGE - Associate Analyst, Data Science Team (Until February 2023).
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

