import pandas as pd

def extract_relevant_citations(query, persona_csv, max_examples=3):
    """
    Given a user query and a persona's CSV, return up to max_examples relevant citations.
    """
    df = pd.read_csv(persona_csv)
    query_lower = query.lower()
    matches = []
    for _, row in df.iterrows():
        text = str(row.get('text', '')).lower()
        if any(word in text for word in query_lower.split()):
            matches.append({
                'character': row.get('character', 'Unknown'),
                'line': row.get('text', ''),
                'movie': row.get('movie_id', 'Unknown'),
                'line_id': row.get('line_id', 'Unknown')
            })
            if len(matches) >= max_examples:
                break
    return matches
