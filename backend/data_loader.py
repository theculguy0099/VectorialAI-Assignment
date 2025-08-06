import os
import pandas as pd

# Define file paths
corpus_path = os.path.join('data', 'cornell movie-dialogs corpus')
lines_path = os.path.join(corpus_path, 'movie_lines.txt')
convos_path = os.path.join(corpus_path, 'movie_conversations.txt')
chars_path = os.path.join(corpus_path, 'movie_characters_metadata.txt')
titles_path = os.path.join(corpus_path, 'movie_titles_metadata.txt')
output_path = os.path.join('data', 'full_dialogues.csv')

# Load and process movie_lines.txt
lines_df = pd.read_csv(lines_path, sep='\+\+\+\$\+\+\+', header=None, engine='python',
                       names=['line_id', 'char_id', 'movie_id', 'char_name', 'text'],
                       encoding='iso-8859-1')
# Clean whitespace from the join key *before* setting it as index
lines_df['line_id'] = lines_df['line_id'].str.strip()
lines_df.set_index('line_id', inplace=True)


# Clean up whitespace
for col in lines_df.columns:
    if lines_df[col].dtype == 'object':
        lines_df[col] = lines_df[col].str.strip()

# Load and process movie_characters_metadata.txt
chars_df = pd.read_csv(chars_path, sep='\+\+\+\$\+\+\+', header=None, engine='python',
                       names=['char_id', 'char_name', 'movie_id', 'movie_title', 'gender', 'position'],
                       encoding='iso-8859-1', index_col='char_id')

# Clean up whitespace
for col in chars_df.columns:
    if chars_df[col].dtype == 'object':
        chars_df[col] = chars_df[col].str.strip()

# Load and process movie_titles_metadata.txt
titles_df = pd.read_csv(titles_path, sep='\+\+\+\$\+\+\+', header=None, engine='python',
                        names=['movie_id', 'movie_title', 'movie_year', 'imdb_rating', 'imdb_votes', 'genres'],
                        encoding='iso-8859-1', index_col='movie_id')

# Clean up whitespace and genres
for col in titles_df.columns:
    if titles_df[col].dtype == 'object':
        titles_df[col] = titles_df[col].str.strip()
titles_df['genres'] = titles_df['genres'].str.replace(r"['\[\]]", "", regex=True)

# Load movie_conversations.txt to get dialogue pairs
conversations = []
with open(convos_path, 'r', encoding='iso-8859-1') as f:
    for line in f:
        parts = line.strip().split(' +++$+++ ')
        char1_id, char2_id, movie_id, line_ids_str = parts
        line_ids = eval(line_ids_str) # Safely evaluate string list
        
        # Create pairs of consecutive lines within a conversation
        for i in range(len(line_ids) - 1):
            line1_id = line_ids[i]
            line2_id = line_ids[i+1]
            conversations.append({'line1_id': line1_id, 'line2_id': line2_id})

convos_df = pd.DataFrame(conversations)


# Merge dataframes to create a full dialogue dataset
# Merge first line info
merged_df = pd.merge(convos_df, lines_df, left_on='line1_id', right_index=True, how='inner')


merged_df.rename(columns={'char_id': 'char1_id', 'char_name': 'char1_name', 'text': 'line1_text', 'movie_id': 'movie_id'}, inplace=True)

# Merge second line info
merged_df = pd.merge(merged_df, lines_df.add_suffix('_2'), left_on='line2_id', right_index=True, how='inner')


merged_df.rename(columns={'char_id_2': 'char2_id', 'char_name_2': 'char2_name', 'text_2': 'line2_text'}, inplace=True)

merged_df.drop(columns=['movie_id_2'], inplace=True)

# Merge movie metadata
merged_df = pd.merge(merged_df, titles_df, on='movie_id', how='left')


# Drop rows with missing values only in essential dialogue columns
merged_df = merged_df.dropna(subset=['line1_text', 'line2_text'])

# Save the processed data
merged_df.to_csv(output_path, index=False)

print(f"Data processing complete. Processed data saved to {output_path}")
