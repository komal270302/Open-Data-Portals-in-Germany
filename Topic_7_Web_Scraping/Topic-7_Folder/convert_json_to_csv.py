import json
import pandas as pd

# Open the JSON data file
with open(r"C:\Users\Dell\Desktop\Topic_7_Web_Scraping\Topic-7_Folder\combined_statistics.json", 'r', encoding='utf-8') as f:
    data = json.load(f)


# Transform JSON into rows of Category, State, Dataset_Count
rows = []
for category, states in data.items():
    for state, count in states.items():
        rows.append({'Category': category, 'State': state, 'Dataset_Count': count})

# Convert to pandas DataFrame
df = pd.DataFrame(rows)

# Save as CSV file
df.to_csv('open_data_categories.csv', index=False)

print("CSV file created successfully!")