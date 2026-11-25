import pandas as pd, json, re, subprocess, os

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
GEM_SVG = "თეა_მეფარიშვილი_24.svg"  # shared placeholder used for Gemini Gem projects

def fix(s):
    s = str(s)
    # Convert Georgian Mtavruli capitals (U+1C90–1CBF) to regular Mkhedruli
    s = "".join(chr(ord(c) - 0x1C90 + 0x10D0) if 0x1C90 <= ord(c) <= 0x1CBF else c for c in s)
    return re.sub(r"\s+", " ", s.replace("\r", " ").replace("\n", " ")).strip()

title_overrides = {
    5: "დაწყებითების მასწავლებელი — მასწავლებლის AI ასისტენტი",
    9: "WordQuest — ინგლისური ენის ლექსიკის ინტერაქტიული ვებ-აპლიკაცია",
}

with open("projects-data.js", encoding="utf-8") as f:
    raw = f.read()
data = json.loads(raw[raw.index("["):raw.rindex("]") + 1])
existing_links = {p["project_link"] for p in data}
next_id = max(p["id"] for p in data) + 1

df = pd.read_excel("Projects.xlsx").dropna(how="all")
new = []
for i, r in df.iterrows():
    if "თანახმა" not in str(r.iloc[14]):
        continue
    links = [p for p in re.split(r"[\s,]+", str(r.iloc[13])) if p.startswith("http")]
    title = title_overrides.get(i, fix(r.iloc[9]))
    # Multiple numbered projects in one submission -> separate cards
    titles = [t.strip(" ;.") for t in re.split(r"\d\.\s*", title) if t.strip(" ;.")] if len(links) > 1 else [title]
    for t, link in zip(titles, links):
        if link in existing_links:
            continue
        name = fix(f"{r.iloc[2]} {r.iloc[3]}")
        img = ""
        if "gemini.google.com/gem" in link:
            img = GEM_SVG
        else:
            img = f"{name.replace(' ', '_')}_{next_id}.png"
            subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--disable-gpu",
                            "--window-size=1440,900", "--virtual-time-budget=8000",
                            f"--screenshot={os.path.abspath(img)}", link],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
            if not os.path.exists(img):
                img = ""
        new.append({
            "id": next_id, "name": name, "region": fix(r.iloc[6]), "school": fix(r.iloc[7]),
            "title": t, "audience": fix(r.iloc[10]), "subjects": fix(r.iloc[11]),
            "description": fix(r.iloc[12]), "project_link": link, "image": img,
        })
        existing_links.add(link)
        next_id += 1

data += new
with open("projects-data.js", "w", encoding="utf-8") as f:
    f.write(f"const projectsData = {json.dumps(data, ensure_ascii=False, indent=2)};")

# Append to the card list in index.html (index in that array == id)
with open("index.html", encoding="utf-8") as f:
    html = f.read()
lines = ",\n".join(
    f'    {{ image: {json.dumps(p["image"], ensure_ascii=False)}, name: {json.dumps(p["name"], ensure_ascii=False)}, '
    f'title: {json.dumps(p["title"], ensure_ascii=False)}, project_link: {json.dumps(p["project_link"])} }}'
    for p in new)
m = re.search(r'(project_link: "[^"]*" \})(\s*\r?\n\s*\];)', html)
html = html[:m.end(1)] + ",\n" + lines + html[m.end(1):]
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

for p in new:
    print(p["id"], p["name"], "|", p["title"], "|", p["image"])

