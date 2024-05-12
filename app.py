import streamlit as st
from groq import Groq

# Set up API key and initialize Groq client
groq_api_key = "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"
groq_client = Groq(api_key=groq_api_key)

# Initial system message explaining the agent's role
system_message = """
You are Isabella, a helpful assistant providing answers on behalf of Pratik S Reddy based on his resume.be snarky.
Name: Pratik S Reddy
Email: Ps41066@gmail.com
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
if "input_buffer" not in st.session_state:
    st.session_state.input_buffer = ""

# Streamlit app UI
st.set_page_config(page_title="Pratik", layout="wide")

st.title("PRATIK REDDY")
st.write("An innovator with a passion for using tools and blending different technologies. I excel in optimizing processes and developing intelligent automation systems with cutting-edge AI. By combining creativity with technical expertise, I revolutionize business and data analytics to deliver high-impact solutions that drive organizational growth.")
st.write("**Talk to Isabella, Pratik's AI Agent**")

# Sidebar details
st.sidebar.write("""
**Pratik Reddy**
- Email: [Ps41066@gmail.com](mailto:Ps41066@gmail.com)
- Location: Bengaluru, India
#- LinkedIn: [Profile](https://www.linkedin.com/in/pratik-reddy-447b531b1/)

""")
#- X: [pratikredy](https://twitter.com/pratikredy)
#- YT: [pratik_AI](https://www.youtube.com/@pratik_AI)
st.sidebar.write("THIS IS A CHATBOT TO GET TO KNOW PRATIK")

st.sidebar.subheader("Professional Summary")
st.sidebar.write("""
Passionate learner skilled in process optimization, automation, and analytics.
Aiming to innovate and implement new ideas for growth.
""")

# Chat history with custom borders but without the larger box
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

# Chat input and submit button below the conversation
user_input = st.text_input("Type your message here:", key="user_input")

if st.button("Send"):
    if user_input:
        # Append user input to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Call Groq API with the entire chat history
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=st.session_state.chat_history,
            temperature=0.3,
            max_tokens=2000
        )
        chatbot_response = response.choices[0].message.content.strip()

        # Append chatbot response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": chatbot_response})

        # Clear the input buffer
        st.session_state.input_buffer = ""
        st.experimental_rerun()

    else:
        st.warning("Please enter some text to chat.")
