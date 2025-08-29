# import json
# import pandas as pd

# with open(r"C:\Users\Dell\Desktop\Topic_7_Web_Scraping\Topic-7_Folder\combined_statistics.json", 'r', encoding='utf-8') as f:
#     data = json.load(f)

# rows = []
# for state, categories in data['States_categories'].items():
#     for entry in categories:
#         rows.append({
#             'State': state,
#             'Category': entry['category'],
#             'Dataset_Count': entry['datasetCount']
#         })

# df = pd.DataFrame(rows)
# df.to_csv('open_data_portal_categories.csv', index=False, encoding='utf-8')
# print("CSV saved successfully!")

import json
import pandas as pd

with open(r"C:\Users\Dell\Desktop\Topic_7_Web_Scraping\Topic-7_Folder\combined_statistics.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

rows = []
for state, categories in data['States_categories'].items():
    for entry in categories:
        rows.append({
            'State': state,
            'Category': entry['category'],
            'Dataset_Count': entry['datasetCount']
        })

df = pd.DataFrame(rows)
print(df)  # Add this to inspect the data
df.to_csv('open_data_portal_categories.csv', index=False, encoding='utf-8')
print("CSV saved successfully!")