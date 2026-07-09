import json

with open('dashboard2.4.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']

        # Backend modification
        if any("def process_stage_data(" in line for line in source):
            # Find the loop over df_clean.iterrows()
            for i, line in enumerate(source):
                if "if 'جميع المناطق' in orig_region:" in line:
                    new_code = [
                        "            if 'جميع المناطق' in city or 'جميع المدن الرئيس' in city:\n",
                        "                new_row = row.copy()\n",
                        "                new_row['cleaned_region'] = 'Global_All' if 'جميع المناطق' in city else 'Global_Main'\n",
                        "                new_row['المنطقة الادارية'] = 'شامل'\n",
                        "                new_row['المدينة'] = city\n",
                        "                expanded_events.append(new_row)\n",
                        "                continue\n",
                        "                \n"
                    ]
                    source = source[:i] + new_code + source[i:]
                    break
            cell['source'] = source

        # Frontend modification: refreshMapColors
        if any("function refreshMapColors()" in line for line in source):
            for i, line in enumerate(source):
                if "targetCounts = { ...stageInfo.counts };" in line:
                    source.insert(i+1, "                let globalAll = stageInfo.counts['Global_All'] || 0;\n")
                    source.insert(i+2, "                let globalMain = stageInfo.counts['Global_Main'] || 0;\n")
                    source.insert(i+3, "                Object.keys(REGION_AR).forEach(r => { targetCounts[r] = (targetCounts[r] || 0) + globalAll + globalMain; });\n")
                    break

            for i, line in enumerate(source):
                if "Object.keys(REGION_AR).forEach(r => { let total = 0; pElements.forEach(el => { stageInfo.events[r]?.forEach(ev => { if(ev.element === el) total++; }); }); targetCounts[r] = total; });" in line:
                    source[i] = "                Object.keys(REGION_AR).forEach(r => { let total = 0; pElements.forEach(el => { stageInfo.events[r]?.forEach(ev => { if(ev.element === el) total++; }); stageInfo.events['Global_All']?.forEach(ev => { if(ev.element === el) total++; }); stageInfo.events['Global_Main']?.forEach(ev => { if(ev.element === el) total++; }); }); targetCounts[r] = total; });\n"
                    break

            for i, line in enumerate(source):
                if "Object.keys(REGION_AR).forEach(r => { let c=0; stageInfo.events[r]?.forEach(ev => { if(ev.element === selectedElementFilter) c++; }); targetCounts[r] = c; });" in line:
                    source[i] = "                Object.keys(REGION_AR).forEach(r => { let c=0; stageInfo.events[r]?.forEach(ev => { if(ev.element === selectedElementFilter) c++; }); stageInfo.events['Global_All']?.forEach(ev => { if(ev.element === selectedElementFilter) c++; }); stageInfo.events['Global_Main']?.forEach(ev => { if(ev.element === selectedElementFilter) c++; }); targetCounts[r] = c; });\n"
                    break

            # Tooltip logic
            for i, line in enumerate(source):
                if "count = stageInfo.counts[r] || 0; totalFilterCount = stageInfo.total || 1;" in line:
                    source[i] = "                                count = (stageInfo.counts[r] || 0) + (stageInfo.counts['Global_All'] || 0) + (stageInfo.counts['Global_Main'] || 0); totalFilterCount = stageInfo.total || 1;\n"
                    break

            # handleRegionClick logic
            for i, line in enumerate(source):
                if "let events = stageInfo.events[regionKey] || [];" in line:
                    source[i] = "                let events = (stageInfo.events[regionKey] || []).concat(stageInfo.events['Global_All'] || []).concat(stageInfo.events['Global_Main'] || []);\n"
                    break

            # renderStageTimeline logic
            for i, line in enumerate(source):
                if "let events = stageInfo.events[regionKey] || [];" in line:
                    source[i] = "            let events = (stageInfo.events[regionKey] || []).concat(stageInfo.events['Global_All'] || []).concat(stageInfo.events['Global_Main'] || []);\n"
                    break

            cell['source'] = source

with open('dashboard2.4.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
