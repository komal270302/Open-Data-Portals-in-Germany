from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import json
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import AgglomerativeClustering

# Load categories from JSON file
with open(r"C:\Users\Dell\Desktop\Topic_7_Web_Scraping\Topic-7_Folder\combined_statistics.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# print("Top-level keys in JSON:", data.keys())

# Navigate into statistics → category_usage_counts
category_usage_counts = data["statistics"]["category_usage_counts"]

# Extract just the category names (keys)
categories = list(category_usage_counts.keys())

print("Loaded categories:", categories)

# Load pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Encode category names into embeddings
embeddings = model.encode(categories, convert_to_tensor=True)

print("Embeddings shape:", embeddings.shape)

# Compute cosine similarity matrix
similarity_matrix = cosine_similarity(embeddings)

# Convert to DataFrame for easier analysis
sim_df = pd.DataFrame(similarity_matrix, index=categories, columns=categories)
print(sim_df.head())

threshold = 0.5
similar_pairs = []

for i in range(len(categories)):
    for j in range(i+1, len(categories)):
        if sim_df.iloc[i, j] > threshold:
            similar_pairs.append((categories[i], categories[j], sim_df.iloc[i, j]))

# Convert to DataFrame
similar_df = pd.DataFrame(similar_pairs, columns=["Category1", "Category2", "Similarity"])
print(similar_df.sort_values(by="Similarity", ascending=False))


plt.figure(figsize=(12, 10))
sns.heatmap(sim_df, cmap="YlGnBu", linewidths=0.5)
plt.title("Category Similarity Heatmap (cosine similarity)")
plt.show()



