import json

with open("dashboard2.4.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        source = "".join(cell["source"])
        if "function refreshMapColors()" in source:
            print(source)
            break
