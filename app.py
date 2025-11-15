# app.py
"""
Yojanasaathi - Streamlit Frontend
Competition Track: Agents for Good
Front-end for welfare scheme conversational assistant (matches your UI image).
"""

import streamlit as st
from agent.core import YojanaAgent  # Main backend agent
import os

# -- PAGE CONFIG --
st.set_page_config(
    page_title="Yojanasaathi",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -- HEADER: Title and Subtitle --
st.markdown(
    "<h1 style='font-family:Arial;'>Yojanasaathi</h1>"
    "<p style='font-size:18px;'>AI-Powered Welfare Scheme Assistant</p>",
    unsafe_allow_html=True
)

# -- Track which language to display (default English) --
if "language" not in st.session_state:
    st.session_state.language = "english"

# -- FRONTEND CATEGORY DEFINITIONS (same as your image) --
categories = [
    {"label": "Education", "icon": "📚"},
    {"label": "Healthcare", "icon": "🗂️"},
    {"label": "Agriculture", "icon": "🌾"},
    {"label": "Women & Child", "icon": "👶"},
    {"label": "Employment", "icon": "💼"},
    {"label": "Housing", "icon": "🏠"},
    {"label": "Senior Citizens", "icon": "👵"},
    {"label": "Disability", "icon": "♿"},
]

# -- Initialize Agent (loads CSV and sets up APIs) --
AGENT = YojanaAgent(
    csv_path=os.path.join("data", "schemes.csv"),
    default_language=st.session_state.language,
)

# -- Category Card Display --
st.markdown("<h3>Browse by Category</h3>", unsafe_allow_html=True)
cols = st.columns(4)
for i, cat in enumerate(categories):
    if cols[i % 4].button(f"{cat['icon']} {cat['label']}"):
        # When category button pressed, enter chat with prefilled category
        response = AGENT.chat(f"Show welfare schemes about {cat['label']}")
        st.session_state.last_answer = response
        st.session_state.last_question = cat['label']

# -- FREETEXT CHAT/QUERY INPUT --
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("Or ask me anything about welfare schemes in the message box below")

with st.form(key="user_input_form", clear_on_submit=True):
    user_inp = st.text_input("Ask about welfare schemes... (e.g., education, farming, women)", key="chat_input")
    submit_pressed = st.form_submit_button("Send")

if submit_pressed and user_inp.strip():
    # Send user query to backend agent, get response in both languages
    st.session_state.last_question = user_inp
    response = AGENT.chat(user_inp)
    st.session_state.last_answer = response

# -- Display Conversation: Show question & dual-language answer --
if "last_answer" in st.session_state and st.session_state.last_answer:
    st.markdown("**You said:** " + str(st.session_state.last_question))
    if isinstance(st.session_state.last_answer, dict):
        # Display answers in both languages
        st.markdown(f"**Answer (English):** {st.session_state.last_answer.get('english', '')}")
        st.markdown(f"**Answer (Hindi):** {st.session_state.last_answer.get('hindi', '')}")
    else:
        st.markdown(st.session_state.last_answer)

# -- CREDIT FOOTER (optional) --
st.markdown(
    "<div style='text-align:center; color:grey;font-size:11px;'>Made with ❤️ for Agents Intensive Capstone</div>",
    unsafe_allow_html=True
)
