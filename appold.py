import streamlit as st
from groq import Groq

# Set up API key and initialize Groq client
groq_api_key = 
groq_client = Groq(api_key=groq_api_key)

# Initial system message
system_message = """
You are a helpful assistant providing answers based on the resume of PRATIK S REDDY.
Name: Pratik S Reddy
Email: Ps41066@gmail.com
Phone: +91-7406056171
Location: Bengaluru, India
LinkedIn: https://www.linkedin.com/in/pratik-reddy-447b531b1/

Professional Summary:
Passionate learner skilled in process optimization, automation, and analytics.
Aiming to innovate and implement new ideas for growth.

Work History:
1. EOX VANTAGE - Associate Analyst, Data Science Team:
    - RPA development, VBA scripting, and AI-powered automation.
    - Web scraping, data extraction, sentiment analysis, and premium rating model development.
    - Leveraged GPT-4 and Azure AI for automation.

2. JUST BAKE - Supply Chain Analyst Intern:
    - Improved supply chain efficiency through data analysis.

3. ORCAD - Intern:
    - Managed multiple stakeholder projects.

Education:
1. Indiana University of Pennsylvania: MBA
2. PES University: BBA
3. Udemy, Google Skillshop: Courses in Python, SQL, GPT API, and Google Ads.

Accomplishments:
- All India Football Federation licensed coach.
- VR video creation and integration with LIDAR data.

Personal Projects:
- Building Web3 dashboards, MP4 subtitling with GPT Whisper, and RPA Finance Tracker.
"""

# Initialize chat history as a session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "system", "content": system_message}]

# Streamlit app UI
st.set_page_config(page_title="Pratik", layout="wide")

st.title("PRATIK REDDY")
st.write("An innovator with a passion for using tools and blending different technologies. I excel in optimizing processes and developing intelligent automation systems with cutting-edge AI. By combining creativity with technical expertise, I revolutionize business analytics to deliver high-impact solutions that drive organizational growth.")
st.write("**Talk to Pratik's AI Agent**")

st.sidebar.title("Resume Details")
st.sidebar.write("""
**Pratik S Reddy**
- Email: [Ps41066@gmail.com](mailto:Ps41066@gmail.com)
- Phone: +91-7406056171
- Location: Bengaluru, India
- LinkedIn: [Profile](https://www.linkedin.com/in/pratik-reddy-447b531b1/)
""")

st.sidebar.subheader("Professional Summary")
st.sidebar.write("""
Passionate learner skilled in process optimization, automation, and analytics.
Aiming to innovate and implement new ideas for growth.
""")

# Chat functionality
user_input = st.text_input("Type your message here:", key="user_input")

if st.button("Send", key="send"):
    if user_input:
        # Update chat history with user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Call Groq API with the entire chat history
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=st.session_state.chat_history,
            temperature=0.3,
            max_tokens=1024
        )
        chatbot_response = response.choices[0].message.content.strip()

        # Update chat history with chatbot response
        st.session_state.chat_history.append({"role": "assistant", "content": chatbot_response})

    else:
        st.warning("Please enter some text to chat.")

# Display chat history with custom borders
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(
            f"<div style='border: 2px solid red; padding: 10px; margin: 10px 0; border-radius: 8px;'>{message['content']}</div>",
            unsafe_allow_html=True
        )
    elif message["role"] == "assistant":
        st.markdown(
            f"<div style='border: 2px solid green; padding: 10px; margin: 10px 0; border-radius: 8px;'>{message['content']}</div>",
            unsafe_allow_html=True
        )

# Ensure the "Send" button remains at the bottom
st.write("")
