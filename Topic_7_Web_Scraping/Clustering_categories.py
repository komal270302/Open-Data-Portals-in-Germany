import json 
from sentence_transformers import SentenceTransformer 
from sklearn.cluster import KMeans 
import umap 
import matplotlib.pyplot as plt 
import seaborn as sns 
import pandas as pd
import plotly.express as px

# 1. Load categories from JSON file # ----------------------- 
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

num_clusters = 7 
kmeans = KMeans(n_clusters=num_clusters, random_state=42) 
cluster_labels = kmeans.fit_predict(embeddings)

# Map categories to cluster labels 
category_clusters = {cat: cluster_labels[i] for i, cat in enumerate(categories)} 
print(category_clusters)

# Reduce embeddings to 2D
reducer = reducer = umap.UMAP(n_neighbors=10, min_dist=0.1, random_state=42)

embeddings_2d = reducer.fit_transform(embeddings)

# Create plotting DataFrame
plot_df = pd.DataFrame({
    "x": embeddings_2d[:, 0],
    "y": embeddings_2d[:, 1],
    "Category": categories,
    "Cluster": cluster_labels
})

fig = px.scatter(
    x=embeddings_2d[:, 0],
    y=embeddings_2d[:, 1],
    color=cluster_labels,
    text=categories
)

fig.update_traces(
    textposition="top center",
    marker=dict(size=10)
)

fig.update_layout(
    title="Open Data Categories – Semantic Clusters",
    showlegend=True
)

fig.show()
