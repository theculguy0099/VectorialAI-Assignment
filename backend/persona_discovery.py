import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

def discover_personas(n_clusters=3, sample_size=20000):
    """Analyzes dialogues to discover personas using clustering."""
    print("Starting persona discovery...")
    
    # Load the processed data
    data_path = os.path.join('data', 'full_dialogues.csv')
    if not os.path.exists(data_path):
        print(f"Error: Processed data file not found at {data_path}")
        print("Please run data_loader.py first.")
        return

    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} dialogues.")

    # Take a sample to speed up processing
    if len(df) > sample_size:
        df = df.sample(n=sample_size, random_state=42)
        print(f"Sampled down to {len(df)} dialogues.")

    # Ensure text column is clean
    df['line1_text'] = df['line1_text'].astype(str).fillna('')

    # Generate embeddings
    print("Generating text embeddings... (This may take a while)")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(df['line1_text'].tolist(), show_progress_bar=True)
    print("Embeddings generated.")

    # Perform K-Means clustering
    print(f"Performing K-Means clustering with {n_clusters} clusters...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df['persona_cluster'] = kmeans.fit_predict(embeddings)
    print("Clustering complete.")

    # Save the dataframe with persona labels
    output_path = os.path.join('data', 'dialogues_with_personas.csv')
    df.to_csv(output_path, index=False)
    print(f"Data with persona clusters saved to {output_path}")

    # Analyze and print samples from each cluster
    for i in range(n_clusters):
        print(f"\n--- Persona Cluster {i} Samples ---")
        cluster_sample = df[df['persona_cluster'] == i].sample(min(5, len(df[df['persona_cluster'] == i])))
        for _, row in cluster_sample.iterrows():
            print(f"  - {row['char1_name']}: {row['line1_text']}")
        
        # Partition data and save
        persona_df = df[df['persona_cluster'] == i]
        persona_output_path = os.path.join('data', f'persona_{i}_data.csv')
        persona_df.to_csv(persona_output_path, index=False)
        print(f"Saved data for persona {i} to {persona_output_path}")

if __name__ == '__main__':
    discover_personas()
