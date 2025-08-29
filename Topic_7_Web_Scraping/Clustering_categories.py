import json
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import umap
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 1. Load categories from JSON file
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

# Convert categories to embeddings
embeddings = model.encode(categories)
print(f"Embedding shape: {embeddings.shape}")

# Define number of clusters (you can tune this)
num_clusters = 8
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
cluster_labels = kmeans.fit_predict(embeddings)

# Map categories to cluster labels
category_clusters = {cat: cluster_labels[i] for i, cat in enumerate(categories)}
print(category_clusters)

# Reduce to 2D
reducer = umap.UMAP(n_neighbors=5, min_dist=0.3, random_state=42)
embeddings_2d = reducer.fit_transform(embeddings)

# Plot
plt.figure(figsize=(12,8))
palette = sns.color_palette("hls", num_clusters)
for i, label in enumerate(set(cluster_labels)):
    idxs = [j for j, x in enumerate(cluster_labels) if x == label]
    plt.scatter(embeddings_2d[idxs,0], embeddings_2d[idxs,1], color=palette[i], label=f"Cluster {label}", s=100)

# Annotate categories
for i, cat in enumerate(categories):
    plt.text(embeddings_2d[i,0]+0.01, embeddings_2d[i,1]+0.01, cat, fontsize=9)

plt.title("Clustering of Open Data Categories (AI/NLP)")
plt.legend()
plt.show()


df = pd.DataFrame({'Category': categories, 'Cluster': cluster_labels})

df.to_csv('category_clusters.csv', index=False)
