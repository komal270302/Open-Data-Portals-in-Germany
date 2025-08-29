import os                        # For file and directory operations
import subprocess                # To run external Python scripts
import json                      # For saving and loading JSON files
import re                        # For regular expression parsing
from collections import Counter  # To count frequency of items
from datetime import datetime

# Folder containing Python scripts to run
folder_path = r"C:\Users\Dell\Desktop\Topic_7_Web_Scraping\Topic-7_Folder"

# Mapping state short names to full names in English as well as German
state_name_map = {
    "Bayern": "Bavaria (Bayern)",
    "Berlin": "Berlin",
    "Brandenburg": "Brandenburg",
    "Bremen": "Bremen",
    "Bw": "Baden-Württemberg",
    "Hamburg": "Hamburg",
    "Hessen": "Hesse(Hessen)",
    "Lower_saxony": "Lower Saxony(Niedersachsen)",
    "Mv": "Mecklenburg-Western Pomerania",
    "Nrw": "North Rhine-Westphalia(Nordrhein-Westfalen)",
    "Rlp": "Rhineland-Palatinate(Rheinland-Pfalz)",
    "Saarland": "Saarland",
    "Saxony": "Saxony(Sachsen)",
    "Saxony-Anhalt": "Saxony-Anhalt(Sachsen-Anhalt)",
    "Schleswig-holstein": "Schleswig-Holstein",
    "Thuringia": "Thuringia(Thüringen)"
}

# Function to extract category names and numbers from script output
def parse_categories(text):
    categories = []
    lines = text.strip().split('\n')
    for line in lines:
        line = line.strip()
        # Skip empty lines or irrelevant text
        if not line or 'Mehr anzeigen' in line or 'Alle anzeigen' in line:
            continue
        # Try to match "CategoryName (123)"
        match = re.match(r'(.+?)\s*\((\d+)\)$', line)
        if not match:
            match = re.match(r'(.+?)\s+(\d+)$', line)
        if match:
            # Try to match "CategoryName 123"
            category = match.group(1).strip()  
            datasetCount = int(match.group(2))       
            categories.append({"category": category, "datasetCount": datasetCount})
    return categories

result = {}      # Holds parsed categories per state
all_categories = []  # Collects all category names (for frequency analysis)
state_category_sets = []  # Stores sets of categories for each state (to find common ones)

# Loop through all Python files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.py'):
        state = filename[:-3]
        file_path = os.path.join(folder_path, filename)
        try:
             # Execute the Python script and capture its output
            process = subprocess.run(
                ['python', file_path],
                capture_output=True,
                text=True
            )
            output = process.stdout
            error = process.stderr

            # If execution was successful and there's output
            if process.returncode == 0 and output:
                categories = parse_categories(output)
                if categories:
                     # Mapping short state name to Full names
                    state_name = state_name_map.get(state, state)
                    result[state_name] = categories

                    # Collect category names for stats
                    category_names = [cat['category'] for cat in categories]
                    all_categories.extend(category_names)  
                    
                     # Save set of categories for common category detection
                    state_category_sets.append(set(category_names))  
                else:
                    print(f"No categories parsed from {filename}")
            else:
                print(f"Error or no output from {filename}:\n{error}")

        except Exception as e:
            print(f"Error running {filename}: {str(e)}")


# STATS: How often is each category used? 
category_counter = Counter(all_categories)

# Parameters to identify common/rare categories  
MOST_USED_LIMIT = 13   
LEAST_USED_LIMIT = 2     

# Get frequently used categories and rarely used categories
most_used_categories = {cat: count for cat, count in category_counter.items() if count >= MOST_USED_LIMIT}
least_used_categories = {cat: count for cat, count in category_counter.items() if count <= LEAST_USED_LIMIT}

# Collect statistics to save
stats = {
    "category_usage_counts": dict(category_counter),
    "most_used_categories (≥{})".format(MOST_USED_LIMIT): most_used_categories,
    "least_used_categories (≤{})".format(LEAST_USED_LIMIT): least_used_categories,
    "common_categories": list(set.intersection(*state_category_sets)) if state_category_sets else []
}

# Convert Counter to regular dict for JSON
stats['category_usage_counts'] = dict(stats['category_usage_counts'])

# Category distribution across states
all_states = list(result.keys())
category_distribution = {}

# Get all unique categories from all states
unique_categories = set(all_categories)

for category in unique_categories:
    present_in = []
    missing_in = []
    for state in all_states:
        state_categories = [cat["category"] for cat in result[state]]
        if category in state_categories:
            present_in.append(state)
        else:
            missing_in.append(state)
    category_distribution[category] = {
        "count": category_counter[category],
        "present_In": present_in,
        "missing_In": missing_in
    }

# Add this distribution data to stats
stats["category_distribution_by_state"] = category_distribution

# Add metadata and save raw categories
categories_with_meta = {
    "createdAt": datetime.now().isoformat(),  
    "usedSoftware": [
        "SODMET (Semantic Open Data Metadata Extraction Tool — umbrella framework)",
        "GovDataScraperTool (Scrapes govdata.de categories with Selenium)",
        "ByDataScraperTool (Scrapes bydata.de scrollable category panel)",
        "BerlinMetaParser (Parses daten.berlin.de categories with BeautifulSoup & Selenium)",
        "CKANMetaFetcher (Fetches CKAN metadata from daten-bw.de API)",
        "NRWCategoryExtractor (Scrapes open.nrw category data with Selenium & BS4)",
        "RLPThemenFetcher (Extracts open.rlp.de thematic data dynamically)"
    ],
    "affiliate": "TU Chemnitz",
    "datasetSources": [
        "https://open.bydata.de/datasets?locale=de&page=1&limit=10",
        "https://daten.berlin.de/datensaetze",
        'https://www.govdata.de/suche?q=brandenburg',
        'https://www.govdata.de/suche?q=bremen',
        "https://www.daten-bw.de/ckan/api/3/action/group_list",
        'https://www.govdata.de/suche?q=Hamburg&sort=relevance_desc&type=all',
        'https://www.govdata.de/suche?q=hessen',
        'https://www.govdata.de/suche?q=lower+saxony',
        'https://www.govdata.de/suche?q=Mecklenburg-Vorpommern',
        "https://open.nrw/suche?volltext=&page=1",
        "https://open.rlp.de/de/suchergebnisse",
        'https://www.govdata.de/suche?q=saarland&sort=relevance_desc&type=all',
        'https://www.govdata.de/suche?q=Saxony-Anhalt',
        'https://www.govdata.de/suche?q=Sachsen',
        'https://www.govdata.de/suche?q=Schleswig-Holstein',
        'https://www.govdata.de/suche?q=thuringia&sort=relevance_desc&type=all'
    ],   
}

# Combine metadata and stats in desired order
combined_statistics = {
    "statistics": {
        "createdAt": categories_with_meta["createdAt"],
        "usedSoftware": categories_with_meta["usedSoftware"],
        "affiliate": categories_with_meta["affiliate"],
        "datasetSources": categories_with_meta["datasetSources"],
        "category_usage_counts": stats["category_usage_counts"],
        f"most_used_categories (≥{MOST_USED_LIMIT})": stats[f"most_used_categories (≥{MOST_USED_LIMIT})"],
        f"least_used_categories (≤{LEAST_USED_LIMIT})": stats[f"least_used_categories (≤{LEAST_USED_LIMIT})"],
        "common_categories": stats["common_categories"],
        "category_distribution_by_state": stats["category_distribution_by_state"], 
    },
    "States_categories" : result
}


# Save combined output to single file
final_output_file = os.path.join(folder_path, 'combined_statistics.json')
with open(final_output_file, 'w', encoding='utf-8') as f:
    json.dump(combined_statistics, f, ensure_ascii=False, indent=2)

print("Successfully saved combined statistics to 'combined_statistics.json'")
