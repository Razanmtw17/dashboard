import json

with open('dashboard2.4.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        if any("KSA_GEOJSON" in line for line in source):
            print("Found KSA_GEOJSON logic")
