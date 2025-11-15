# agent/core.py
"""
Yojanasaathi Main Backend Agent
Handles multi-turn chat, scheme matching, Gemini/OpenAI integration, session, dual-language output.
"""

import os
from agent.matcher import match_schemes   # Fuzzy/semantic scheme matcher
from agent.translator import translate    # Translation (English/Hindi)
from agent.memory import Memory           # Conversation/session tracker

# Setup for Gemini/OpenAI integration (tool use concept)
try:
    import google.generativeai as genai
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
except ImportError:
    genai = None
    GEMINI_API_KEY = ""

class YojanaAgent:
    """
    Main agent class for welfare scheme assistant.
    Supports multi-turn conversational matching with memory and tool use.
    """
    def __init__(self, csv_path, default_language="english"):
        """
        Args:
            csv_path (str): Path to the welfare schemes CSV file.
            default_language (str): Response language.
        """
        self.csv_path = csv_path
        self.memory = Memory()
        self.default_language = default_language
        self.schemes = self._load_schemes(csv_path)
        self.llm_on = bool(GEMINI_API_KEY)
        if self.llm_on:
            genai.configure(api_key=GEMINI_API_KEY)
            self.llm_model = genai.GenerativeModel("gemini-pro")
        else:
            self.llm_model = None  # fallback to simple retrieval if API missing

    def _load_schemes(self, path):
        # Loads schemes from CSV, returns a pandas DataFrame
        import pandas as pd
        try:
            return pd.read_csv(path)
        except Exception as e:
            print("Error loading schemes:", e)
            return pd.DataFrame()

    def chat(self, user_query):
        """
        Main chat logic for multi-turn conversation.
        Args:
            user_query (str): Raw user input/question.
        Returns:
            dict: {'english': ..., 'hindi': ...}
        """
        # -- Store user input in memory --
        self.memory.add_user_input(user_query)
        context = self.memory.get_session_context()

        # -- If LLM/Tool available, use it to clarify or refine user query --
        if self.llm_model:
            refined_query = self._refine_query_llm(user_query, context)
        else:
            refined_query = user_query

        # -- Match best schemes using matcher agent --
        matches = match_schemes(refined_query, self.schemes, context)

        # -- Build formatted answer in English --
        answer_en = self._format_schemes_answer(matches, lang="english")
        # -- Translate to Hindi using translator agent --
        answer_hi = translate(answer_en, lang="hindi")

        # -- Store agent output in memory --
        self.memory.add_agent_output(answer_en, answer_hi)

        return {"english": answer_en, "hindi": answer_hi}

    def _refine_query_llm(self, query, context):
        """
        Uses LLM tool (Gemini) to clarify or improve user query based on session context.
        """
        prompt = f"User input: {query}\nPrevious inputs: {context}\nClarify the user's intent for matching welfare schemes."
        try:
            response = self.llm_model.generate_content(prompt)
            return response.text if hasattr(response, "text") else str(response)
        except Exception as e:
            print("Gemini error:", e)
            return query

    def _format_schemes_answer(self, matches, lang="english"):
        """
        Formats matched schemes for chat display.
        Args:
            matches (list): List of matched scheme dicts.
            lang (str): Language of output.
        Returns:
            str: Chat answer.
        """
        if not matches:
            return "No relevant welfare scheme found. Please try again with more details."
        msg_lines = []
        for i, sch in enumerate(matches[:5]):  # Show up to 5
            msg_lines.append(f"{i+1}. {sch.get('schemename','')}\n{sch.get('details','')}\nEligibility: {sch.get('eligibility','')}\nBenefits: {sch.get('benefits','')}\n---")
        return "\n".join(msg_lines)

# End of agent/core.py
