Yojanasaathi: AI-Powered Welfare Scheme Assistant
Track: Agents for Good – Civic Technology/Social Welfare
Project Goal:
Helping citizens identify the best-fit welfare schemes from 3000+ government initiatives by conversationally matching their needs and eligibility.

Features
1. Category-based UI: Quick browse for Education, Healthcare, Agriculture, Women & Child, Employment, Housing, Senior Citizens, Disability

2. Conversational agent: Multi-turn chat, both category click and message box input

3. Intelligent matching: AI/LLM (Gemini) matches user scenario to welfare scheme from CSV

4. Dual language: Responds in both English and Hindi

5. Multi-agent architecture: LLM for query refinement, CSV agent for filtering, translation agent

6. Session memory: Remembers context across conversation (eligibility, preferences)

7. Tool-use: Gemini API, CSV/document parsing, translation services

8. Ready for competition: Fully commented, modular, easy to run in Streamlit (web) and CLI/Notebook

9. Deployment: Streamlit for demo, modular backend for future web/mobile/CLI adaptation

Folder Structure

yojanasaathi/
│
├── app.py                  # Main Streamlit UI app
├── agent/
│   ├── __init__.py
│   ├── core.py             # Agent core (chat, session, LLM/API)
│   ├── matcher.py          # Scheme match/filter logic
│   ├── translator.py       # English/Hindi output
│   └── memory.py           # Session/context state management
├── data/
│   ├── schemes.csv         # Welfare schemes data
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── utils/
    ├── __init__.py
    └── file_utils.py       # Data loaders/helpers
Getting Started
Install dependencies


pip install -r requirements.txt
(Optional) Set Gemini API Key

Put your Gemini API key in a .env file or set as an environment variable:


GEMINI_API_KEY=YOUR_KEY_HERE
Launch the Streamlit app


streamlit run app.py
or in Colab/Jupyter, import and use agent.core for CLI demo.

Usage

Click a category or type a question in chat (English or Hindi)

See best-matched schemes with details, eligibility, steps, and documents

How it works
Multi-agent system: Each query is refined by an LLM (Gemini/OpenAI), sent to a document-matching agent, and results are translated.

Session memory: User context is tracked (age, gender, location, etc.) and used for accurate matching.

Tool use: Uses LLM APIs for NLU/translation and CSV parsing for rapid document lookup.

Observability: Includes logging and verbose comments in all code for technical design review.

Code Quality
Each Python file features docstrings and line-by-line comments.

Modular functions for easy readability and expansion.

README covers submission requirements for the Kaggle Capstone.

Customization
Data file (schemes.csv) can be updated with real government data.

Hindi/English translation logic is modular; add more languages as needed.

UI styling in app.py can be adjusted for look & feel.

License
Open source for educational and civic good.