import json

with open('dashboard2.4.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        if any("counts_dict = {r: 0 for r in ALL_REGIONS}" in line for line in source):
            for i, line in enumerate(source):
                if "counts_dict['International'] = 0" in line:
                    source.insert(i+1, "        counts_dict['Global_All'] = 0\n")
                    source.insert(i+2, "        counts_dict['Global_Main'] = 0\n")
                    break
            cell['source'] = source

with open('dashboard2.4.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
