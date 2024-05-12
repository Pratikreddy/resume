import streamlit as st
from groq import Groq

# Set up API key and initialize Groq client
groq_api_key = "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"
groq_client = Groq(api_key=groq_api_key)

# Initial system message
system_message = """
You are a helpful assistant providing answers based on the resume of PRATIK S REDDY.
Name: Pratik S Reddy
Email: Ps41066@gmail.com
Phone: +91-7406056171
Location: Bengaluru, India
LinkedIn: https://www.linkedin.com/in/pratik-reddy

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

# List to hold chat history
chat_history = []

# Streamlit app UI
st.set_page_config(page_title="Pratik", layout="wide")

st.title("PRATIK REDDY")
st.write("An innovator with a passion for using tools and blending different technologies. I excel in optimizing processes and developing intelligent automation systems with cutting-edge AI. By combining creativity with technical expertise, I revolutionize business analytics to deliver high-impact solutions that drive organizational growth.")
st.write("**Talk to Pratiks AI AGENT**")

st.sidebar.title("Resume Details")
st.sidebar.write("""
**Pratik S Reddy**
- Email: [Ps41066@gmail.com](mailto:Ps41066@gmail.com)
- Phone: +91-7406056171
- Location: Bengaluru, India
- LinkedIn: [Profile](https://www.linkedin.com/in/pratik-reddy)
""")

st.sidebar.subheader("Professional Summary")
st.sidebar.write("""
Passionate learner skilled in process optimization, automation, and analytics.
Aiming to innovate and implement new ideas for growth.
""")

# Chat functionality
#st.subheader("Chat with the Resume Chatbot")
user_input = st.text_input("Type your message here:", key="user_input")

if st.button("Send", key="send"):
    if user_input:
        # Update chat history with user message
        chat_history.append(f"You: {user_input}")

        # Call Groq API
        messages = [{"role": "system", "content": system_message}]
        messages.extend({"role": "user", "content": msg.split(': ', 1)[1]} for msg in chat_history if msg.startswith("You:"))
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages,
            temperature=0.3,
            max_tokens=1024
        )
        chatbot_response = response.choices[0].message.content.strip()

        # Update chat history with chatbot response
        chat_history.append(f"Chatbot: {chatbot_response}")

    else:
        st.warning("Please enter some text to chat.")

# Display chat history
for message in chat_history:
    if message.startswith("You:"):
        st.text_area("", message, height=45, key=message[:10], help="Your message")
    else:
        st.text_area("", message, height=100, key=message[:10], help="Chatbot's response")


