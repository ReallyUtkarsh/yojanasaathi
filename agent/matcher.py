# agent/matcher.py
"""
Scheme Matcher Agent for Yojanasaathi
Intelligently filters and ranks welfare schemes from user query and conversation context.
Uses basic keyword, semantic, and context-based filtering.
"""

import re
from sentence_transformers import SentenceTransformer, util

# Load pre-trained semantic model for fuzzy matching (fast/lightweight)
MODEL = SentenceTransformer('all-MiniLM-L6-v2')

def match_schemes(user_query, schemes_df, context=None, top_n=5):
    """
    Main matching function for welfare schemes.
    Args:
        user_query (str): User's refined question.
        schemes_df (pd.DataFrame): Loaded CSV dataframe of schemes.
        context (str): Prior chat context for more accuracy.
        top_n (int): Number of top schemes to return.
    Returns:
        list: List of best match schemes (dicts ready for display).
    """
    # 1. Combine query and prior context for search (key for multi-turn)
    query = user_query
    if context:
        query += " " + context

    # 2. Semantic embedding of user query for document search
    user_emb = MODEL.encode([query])[0]
    scheme_texts = schemes_df['details'].fillna("") + " " + schemes_df['schemename'].fillna("")
    scheme_embs = MODEL.encode(scheme_texts.tolist())

    # 3. Score similarity (cosine) and rank all schemes
    sims = util.cos_sim(user_emb, scheme_embs).flatten()
    top_idx = sims.argsort()[-top_n:][::-1]
    matches = [schemes_df.iloc[i].to_dict() for i in top_idx]

    # 4. Filter out low-score matches if irrelevant
    min_sim = 0.2
    filtered = []
    for i, idx in enumerate(top_idx):
        if sims[idx] >= min_sim:
            filtered.append(schemes_df.iloc[idx].to_dict())
    if not filtered:  # fallback to keyword search if all fail
        filtered = _keyword_match(user_query, schemes_df, top_n)
    return filtered

def _keyword_match(query, schemes_df, top_n=3):
    """
    Simple fallback: Matches query words in scheme name or tags.
    """
    matches = []
    words = set(re.findall(r"\w+", query.lower()))
    for _, row in schemes_df.iterrows():
        name = str(row.get('schemename', '')).lower()
        tags = str(row.get('tags', '')).lower()
        if any(w in name or w in tags for w in words):
            matches.append(row.to_dict())
            if len(matches) >= top_n:
                break
    return matches

# End of agent/matcher.py
