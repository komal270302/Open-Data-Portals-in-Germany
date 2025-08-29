# Overview
This project automates the collection, processing, and analysis of dataset categories from the open data portals of Germany's 16 federal states. It addresses the lack of standardization in category usage across portals by scraping data, storing it in structured formats (JSON and CSV), performing statistical analysis, and applying AI-driven techniques for similarity detection and clustering. The goal is to provide insights into category frequency, distribution, over/underrepresentation, and semantic similarities, supporting better metadata standardization and policy discussions.
This work was conducted as a research internship at TU Chemnitz (Germany).

# Motivation 
Open data portals promote transparency, innovation, and public access to government datasets. Categories (e.g., "Umwelt" for environment or "Verkehr" for transport) help users navigate datasets effectively. However, German state portals use inconsistent categories, making cross-state comparisons challenging. This project automates category extraction to enable statistical analysis (e.g., most/least used categories), Identify common categories across states and Use AI to detect semantically similar categories for potential standardization.

# Features
1. Web Scraping: Automated extraction of categories and dataset counts from 16 state portals using dynamic (Selenium) and static (BeautifulSoup, Requests) methods with robust error handling.
2. Data Storage: Results standardized into JSON for scalability and CSV for easy analysis.
3. Statistical Analysis: Computes category usage counts, most/least used categories, common categories across states, and per-state distribution.
4. AI-Driven Insights: Uses pre-trained NLP embeddings (SentenceTransformer) to identify semantically similar categories via cosine similarity.
5. Visualization: Generates heatmaps (Matplotlib, Seaborn) for similarities, 2D cluster plots (UMAP, KMeans), and interactive Power BI dashboards for KPI tracking (e.g., category distributions).
6. Focus on Quality: Emphasizes data accuracy, reproducibility, and error handling.

# Technologies Used
1. Programming Language: Python
2. Web Scraping: Selenium (for dynamic content), BeautifulSoup (HTML parsing), Requests (API fetching)
3. Data Processing: Pandas, JSON, Counter (from collections)
4. AI/NLP: SentenceTransformer (for embeddings), scikit-learn (cosine similarity, KMeans clustering), UMAP (dimensionality reduction)
5. Visualization: Matplotlib, Seaborn
6. Other: re (regular expressions), datetime, os, subprocess

# Project Structure 
1. State-Specific Scrapers (16 files, one per German federal state, e.g., Bayern.py, Berlin.py, Brandenburg.py, etc.): Individual scripts to scrape categories from each state's open data portal.
2. All_state.py: Main orchestration script that runs all state scrapers, parses outputs, computes statistics (e.g., frequency, most/least used, common categories, distribution), and saves everything to combined_statistics.json.
3. AI.py: Computes semantic similarities between categories using NLP embeddings, generates a cosine similarity matrix, identifies similar pairs (threshold > 0.5), and creates a heatmap visualization.
4. Clustering_categories.py: Performs KMeans clustering on category embeddings, reduces to 2D with UMAP, and generates a scatter plot visualization. Outputs clusters to category_clusters.csv.
5. convert_json_to_csv.py: Converts the JSON output to a CSV file (open_data_portal_categories.csv) for easier data exploration.
6. combined_statistics.json: Central output file containing raw category data per state, metadata (e.g., creation date, software used, sources), and computed statistics (e.g., category_usage_counts, most_used_categories, category_distribution_by_state).
7. open_data_portal_categories.csv: CSV export of categories, states, and dataset counts.
8. category_clusters.csv: CSV of categories mapped to their AI-generated clusters.
9. Open data portal.pbit: Power BI template file containing interactive dashboards for visualizing category distributions, usage statistics, and other key metrics derived from open_data_portal_categories.csv.

# Setup and Installation
1. Clone the Repository: git clone https://github.com/komal270302/Open-Data-Portals-in-Germany.git
                         cd Open-Data-Portals-in-Germany

2. Install Dependencies: Create a requirements.txt file with the following (or install manually):
   selenium
   beautifulsoup4
   requests
   pandas
   sentence-transformers
   scikit-learn
   umap-learn
   matplotlib
   seaborn

Then run: pip install -r requirements.txt

3. Configure Paths: Scripts use hardcoded paths like C:\Users\Dell\Desktop\Topic_7_Web_Scraping\Topic-7_Folder. Update these to match your local setup. Ensure ChromeDriver is installed and in your PATH for Selenium (download from chromedriver.chromium.org).

# How to Run
1. Scrape and Generate Statistics: Run python All_state.py - This runs all 16 state scrapers sequentially. Scraping may take time due to dynamic portals.
Outputs: combined_statistics.json (raw data + stats).

2. Convert JSON to CSV: Run python convert_json_to_csv.py
Outputs: open_data_portal_categories.csv

3. AI Similarity Analysis: Run python AI.py - Loads data from JSON.
Outputs: Similarity DataFrame (printed), heatmap visualization.

4. Category Clustering:Run python Clustering_categories.py
Outputs: Cluster mappings (printed), 2D visualization plot, category_clusters.csv.

5. Power BI Dashboards: Open Open data portal.pbit in Power BI Desktop. Ensure open_data_portal_categories.csv is available in the same directory or update the data source within Power BI.

# Results and Insights 
1. Example Stats (from JSON/CSV): Categories like "Umwelt" (Environment) are widely used across states, while others like "Internationale Themen" are underrepresented.
2. Similarities: AI detects pairs like "Verkehr" and "Mobilität / Verkehr" with high cosine similarity.
3. Clusters: Categories grouped into ~8 clusters (e.g., education/sports, environment/health).
4. Visuals: Heatmaps show similarity patterns; 2D plots reveal clusters; Power BI dashboards provide interactive exploration of category usage and distribution across states.

# Contributor
Komal (komal202220@gmail.com)

