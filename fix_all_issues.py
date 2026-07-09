import json
import re

with open("dashboard2.4.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        source = "".join(cell["source"])
        changed = False

        # 1. Revert 'المسار الدولي' and appending `- دولي` or `- رقمي`
        if "if orig_region == 'أخرى' or orig_region == 'اخرى':" in source:
            old_str = """            if orig_region == 'أخرى' or orig_region == 'اخرى':
                new_row = row.copy()
                new_row['cleaned_region'] = 'International'
                new_row['المنطقة الادارية'] = 'دولي'
                new_row['المدينة'] = city
                if 'العنصر' in new_row and pd.notna(new_row['العنصر']):
                    new_row['العنصر'] = str(new_row['العنصر']).strip() + " - دولي"
                expanded_events.append(new_row)
                continue"""
            new_str = """            if orig_region == 'أخرى' or orig_region == 'اخرى':
                new_row = row.copy()
                new_row['cleaned_region'] = 'International'
                new_row['المنطقة الادارية'] = 'أخرى'
                new_row['المدينة'] = city
                expanded_events.append(new_row)
                continue"""
            if old_str in source:
                source = source.replace(old_str, new_str)
                changed = True

        # Add the 'رقمي' mapping without suffix
        if "if orig_region == 'أخرى' or orig_region == 'اخرى':" in source and "if orig_region == 'رقمي':" not in source:
            new_str = """            if orig_region == 'أخرى' or orig_region == 'اخرى':
                new_row = row.copy()
                new_row['cleaned_region'] = 'International'
                new_row['المنطقة الادارية'] = 'أخرى'
                new_row['المدينة'] = city
                expanded_events.append(new_row)
                continue

            if orig_region == 'رقمي':
                new_row = row.copy()
                new_row['cleaned_region'] = 'Digital'
                new_row['المنطقة الادارية'] = 'رقمي'
                new_row['المدينة'] = city
                expanded_events.append(new_row)
                continue"""

            source = source.replace("""            if orig_region == 'أخرى' or orig_region == 'اخرى':
                new_row = row.copy()
                new_row['cleaned_region'] = 'International'
                new_row['المنطقة الادارية'] = 'أخرى'
                new_row['المدينة'] = city
                expanded_events.append(new_row)
                continue""", new_str)
            changed = True

        if 'base_el = el.replace(" - دولي", "")' in source:
            old_str = """            base_el = el.replace(" - دولي", "")
            if el.endswith(" - دولي"):
                p_name = "المسار الدولي"
            else:
                p_name = el_to_path.get(el, el_to_path.get(base_el, "مسارات عامة"))
                if p_name == "nan" or p_name == "" or pd.isna(p_name): p_name = "مسارات عامة\""""
            new_str = """            base_el = el
            p_name = el_to_path.get(el, el_to_path.get(base_el, "مسارات عامة"))
            if p_name == "nan" or p_name == "" or pd.isna(p_name): p_name = "مسارات عامة\""""
            if old_str in source:
                source = source.replace(old_str, new_str)
                changed = True

        # 2. Dim Overlay Javascript implementation
        if "function refreshMapColors()" in source:
            old_str = """        function refreshMapColors() {"""
            new_str = """        function refreshMapColors() {
            let overlay = document.getElementById("map-overlay");
            if (overlay) overlay.style.display = 'none';
            if (selectedElementFilter) {
                const stageInfo = STAGES_DATA[currentStage];

                let totalEvents = 0;
                let digitalCount = 0;
                let intlCount = 0;

                Object.keys(stageInfo.events).forEach(reg => {
                    if (stageInfo.events[reg]) {
                        stageInfo.events[reg].forEach(e => {
                            if (e.element === selectedElementFilter) {
                                totalEvents++;
                                if (reg === 'Digital') {
                                    digitalCount++;
                                } else if (reg === 'International') {
                                    intlCount++;
                                }
                            }
                        });
                    }
                });

                if (totalEvents > 0 && digitalCount === totalEvents) {
                    if (overlay) { overlay.style.display = 'flex'; overlay.textContent = 'مخرج رقمي'; }
                } else if (totalEvents > 0 && intlCount === totalEvents) {
                    if (overlay) { overlay.style.display = 'flex'; overlay.textContent = 'مخرج دولي'; }
                }
            }"""

            # remove existing overlay logic to avoid duplication
            if 'let overlay = document.getElementById("map-overlay");' not in source:
                source = source.replace(old_str, new_str)
                changed = True

        # 3. Solid color for "العملات التذكارية"
        if "updateLegendUI(` زخم عنصر: ${selectedElementFilter}`," in source:
            old_str = """                updateLegendUI(` زخم عنصر: ${selectedElementFilter}`, customScales, thresholds);
                Object.keys(REGION_AR).forEach(r => {
                    const count = targetCounts[r] || 0;
                    document.querySelectorAll(`.gov-path[data-region="${r}"]`).forEach(p => p.setAttribute('fill', getHeatColorValue(count, thresholds, customScales)));
                    document.querySelectorAll(`text[data-region-text="${r}"]`).forEach(t => t.setAttribute('fill', count >= thresholds[1] ? "#ffffff" : "#1e3d59"));
                });"""

            new_str = """                let isCommemorative = selectedElementFilter && selectedElementFilter.includes("العملات التذكارية");
                updateLegendUI(` زخم عنصر: ${selectedElementFilter}`, customScales, thresholds);
                Object.keys(REGION_AR).forEach(r => {
                    const count = targetCounts[r] || 0;
                    document.querySelectorAll(`.gov-path[data-region="${r}"]`).forEach(p => p.setAttribute('fill', isCommemorative ? customScales[4] : getHeatColorValue(count, thresholds, customScales)));
                    document.querySelectorAll(`text[data-region-text="${r}"]`).forEach(t => t.setAttribute('fill', count >= thresholds[1] ? "#ffffff" : "#1e3d59"));
                });"""
            if old_str in source:
                source = source.replace(old_str, new_str)
                changed = True

        # 4. Active state CSS + JS
        if ".org-card-item" in source or ".city-progress-card {" in source:
            if ".active-modal-item" not in source:
                old_str = ".city-progress-card:hover { border-color:#1e3d59; transform: translateY(-2px); box-shadow: 0 5px 10px rgba(0,0,0,0.05); }"
                new_str = ".city-progress-card:hover { border-color:#1e3d59; transform: translateY(-2px); box-shadow: 0 5px 10px rgba(0,0,0,0.05); }\n        .active-modal-item { border-color: #ff6f3c !important; background: #fff7f5 !important; transform: translateX(-3px); box-shadow: 0 4px 10px rgba(255,111,60,0.15) !important; }"
                source = source.replace(old_str, new_str)
                changed = True

        if "function filterTimelineByCity(cityName)" in source:
            old_str = """        function filterTimelineByCity(cityName) {
            document.getElementById('modal-timeline-title').textContent = " تقويم مخرجات مدينة: " + cityName;
            renderStageTimeline(currentOpenRegionKey, cityName);
            document.getElementById('clear-city-filter-btn').style.display = 'inline-block';
        }"""
            new_str = """        function filterTimelineByCity(cityName, el) {
            document.querySelectorAll('.city-progress-card').forEach(c => c.classList.remove('active-modal-item'));
            if(el) el.classList.add('active-modal-item');
            document.getElementById('modal-timeline-title').textContent = " تقويم مخرجات مدينة: " + cityName;
            renderStageTimeline(currentOpenRegionKey, cityName);
            document.getElementById('clear-city-filter-btn').style.display = 'inline-block';
        }"""
            if old_str in source:
                source = source.replace(old_str, new_str)
                changed = True

        if "function renderOrgEvents(orgName, elName)" in source:
            old_str = """        function renderOrgEvents(orgName, elName) {
            const tableContainer = document.getElementById('org-events-table-container');"""
            new_str = """        function renderOrgEvents(orgName, elName, el) {
            document.querySelectorAll('.org-card-item').forEach(c => c.classList.remove('active-modal-item'));
            if(el) el.classList.add('active-modal-item');
            const tableContainer = document.getElementById('org-events-table-container');"""
            if old_str in source:
                source = source.replace(old_str, new_str)
                changed = True

        if "onclick=\"filterTimelineByCity('${city}')\"" in source:
            source = source.replace("onclick=\"filterTimelineByCity('${city}')\"", "onclick=\"filterTimelineByCity('${city}', this)\"")
            changed = True

        if "onclick=\"renderOrgEvents(null, '${elName}')\"" in source:
            source = source.replace("onclick=\"renderOrgEvents(null, '${elName}')\"", "onclick=\"renderOrgEvents(null, '${elName}', this)\"")
            changed = True

        if "onclick=\"renderOrgEvents('${org}', '${elName}')\"" in source:
            source = source.replace("onclick=\"renderOrgEvents('${org}', '${elName}')\"", "onclick=\"renderOrgEvents('${org}', '${elName}', this)\"")
            changed = True

        # 5. Map stroke color to black
        if '.gov-path { stroke:#1e3d59;' in source:
            source = source.replace('.gov-path { stroke:#1e3d59;', '.gov-path { stroke:#000000;')
            changed = True

        if changed:
            lines = source.split("\n")
            new_lines = [line + "\n" for line in lines[:-1]] + [lines[-1]]
            cell["source"] = new_lines

with open("dashboard2.4.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
