import json

with open("dashboard2.4.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        source = "".join(cell["source"])
        changed = False

        if "function refreshMapColors()" in source:
            old_str = """        function handleElementRowClick(elementName, event) {
            event.stopPropagation();
            if(currentStage === 'comparison') return;
            selectedPathFilter = null; document.querySelectorAll('.path-container').forEach(p => p.classList.remove('active-path-filter'));
            const rowId = "el-row-" + btoa(unescape(encodeURIComponent(elementName))).replace(/=/g, '');
            if (selectedElementFilter === elementName) {
                selectedElementFilter = null; document.getElementById(rowId).classList.remove('active-element-filter');
                renderGallery([]);
            } else {
                document.querySelectorAll('.element-row').forEach(r => r.classList.remove('active-element-filter')); selectedElementFilter = elementName; document.getElementById(rowId).classList.add('active-element-filter');
                if (currentStage === 'execution') {
                    const elImgs = ELEMENT_IMAGES_EXEC[elementName] || [];
                    renderGallery(elImgs);
                } else {
                    renderGallery([]);
                }
            }
            refreshMapColors();
        }"""
            # Wait, `refreshMapColors();` is ALREADY at the end of `handleElementRowClick`.
            # Let me check `handlePathHeaderClick`. I added `refreshMapColors()` to `handlePathHeaderClick`.
            # Let me verify what the user says:
            # "عند الضغط على "مسار" من السايد بانل، تتحدث منطقة الرياض فقط ولا تتحدث باقي مناطق الخريطة."
            # Why would it update Riyadh only?
            # Let's check `refreshMapColors` -> `selectedPathFilter` block.

            old_str_2 = """            } else if (selectedPathFilter) {
                const pElements = Object.keys(stageInfo.hierarchy[selectedPathFilter]["elements"]);
                const customScales = generateChoroplethScales(PATH_COLORS[selectedPathFilter] || "#b85c38");
                Object.keys(REGION_AR).forEach(r => { let total = 0; pElements.forEach(el => { stageInfo.events[r]?.forEach(ev => { if(ev.element === el) total++; }); }); targetCounts[r] = total; });"""
            # "Object.keys(REGION_AR).forEach(r => { let total = 0; pElements.forEach(el => { stageInfo.events[r]?.forEach(ev => { if(ev.element === el) total++; }); }); targetCounts[r] = total; });"
            # This logic calculates `targetCounts` for the path correctly.
            # Why would it only update Riyadh?
            # Maybe `stageInfo.events` doesn't have events for other regions? No, that's backend.
            # Let's check `pElements` computation. `stageInfo.hierarchy[selectedPathFilter]["elements"]` is built from `raw_counts`.
            # Wait! For the backend Python:
            # The user says: "العناصر التي تحتوي على مخرجات مكانية جغرافية وفي نفس الوقت تحتوي على مخرجات "أخرى" (دولي) أو "رقمي" تتسبب في تعطل الواجهة."
            # They also said: "قم بفصل المخرجات الدولية في السايد بانل كعنصر جديد باسم [اسم العنصر] - دولي، وضعه تحت نفس المسار الأصلي (لا تنشئ مسارات جديدة). إذا كان العنصر "مختلطاً" (يحتوي على مناطق جغرافية + "رقمي"): قم بفصل المخرجات الرقمية كعنصر جديد باسم [اسم العنصر] - رقمي، تحت نفس المسار الأصلي."
            # Aha! I reverted this previously! The user now explicitly wants the `- دولي` and `- رقمي` suffixes BACK, but they want the path to remain the original path!
            pass
