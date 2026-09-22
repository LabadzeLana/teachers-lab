import pandas as pd
import json
import re

# We will recreate the image mapping dictionary based on the verified run
image_mapping = {
    0: "ანა ნათენაძე.png",
    1: "ანა ბელქანია.png",
    2: "დიანა_მაკალათია_2.svg",
    3: "ზინაიდა დვალიშვილი.png",
    4: "ზინაიდა_დვალიშვილი_4.png",
    5: "ეკა_კევლიშვილი_5.svg",
    6: "ეკა კევლიშვილი.png",
    7: "ელიზა_ბაგალიშვილი_7.svg",
    8: "ელიზა_ბაგალიშვილი_8.png",
    9: "ელზა_მოსეშვილი_9.svg",
    10: "ეთერ_მაისურაძე_10.svg",
    11: "რუსუდან_გორგაძე_11.svg",
    12: "ჟუჟუნა_ბარამაშვილი_12.svg",
    13: "ლელა_ლელაძე_13.png",
    14: "ხატია_პარსალიშვილი_14.png",
    15: "ქრისტინა_ქუთათელაძე_15.svg",
    16: "მარი_ჩახვაშვილი_16.png",
    17: "მაკა_კალანდაძე_17.svg",
    18: "მარიამი_ბერია_18.png",
    19: "მარიამ_მაჭარაშვილი_19.png",
    20: "ნატო_სომხიშვილი_20.png",
    21: "ფიქრია_გაბრიჭიძე_21.png",
    22: "ქეთევან_გაბლიშვილი_22.svg",
    23: "ქეთევან_გაბლიშვილი_23.png",
    24: "თეა_მეფარიშვილი_24.svg"
}

df = pd.read_excel('პროექტები.xlsx')
records = []

for i, r in df.iterrows():
    consent = str(r.iloc[14]).strip()
    if 'თანახმა' in consent:
        first_name = str(r.iloc[2]).strip()
        last_name = str(r.iloc[3]).strip()
        name = f"{first_name} {last_name}"
        
        region = str(r.iloc[6]).strip()
        school = str(r.iloc[7]).strip()
        title = str(r.iloc[9]).strip()
        audience = str(r.iloc[10]).strip()
        subjects = str(r.iloc[11]).strip()
        description = str(r.iloc[12]).strip()
        
        # Link clean up
        link = str(r.iloc[13]).strip()
        parts = link.replace('\n', ' ').replace(',', ' ').split(' ')
        links = [p.strip() for p in parts if p.strip().startswith('http')]
        primary_link = links[0] if links else link
        
        # Original 4 specific adjustments
        if name == "ანა ბელქანია" and i == 1:
            title = "ChemDetective — ვირტუალური ქიმიის ლაბორატორია"
            primary_link = "https://anabelkania.github.io/-Chemistry/"
        elif name == "ანა ნათენაძე" and i == 0:
            title = "იგავ-არაკი — სულხან-საბა ორბელიანის „ენით დაკოდილი“"
            primary_link = "https://aniinatenadze-byte.github.io/enit_dakodili/"
        elif name == "ეკა კევლიშვილი" and i == 6:
            title = "ციფრული მოქალაქეობის ინტერაქტიული ქვიზი"
            primary_link = "https://ekakevli1981.github.io/-/"
        elif name == "ზინაიდა დვალიშვილი" and i == 3:
            title = "უსაფრთხო ინტერნეტი — ციფრული მოქალაქეობა"
            primary_link = "https://dvalishvilizika-sys.github.io/usafrtxo_interneti/#hero"
            
        title = title.replace('\n', ' ').replace('\r', '').replace('  ', ' ')
        title = re.sub(r'\s+', ' ', title).strip()
        
        # Clean other fields
        region = region.replace('\n', ' ').strip()
        school = school.replace('\n', ' ').strip()
        audience = audience.replace('\n', ' ').strip()
        subjects = subjects.replace('\n', ' ').strip()
        description = description.replace('\n', ' ').replace('\r', ' ')
        description = re.sub(r'\s+', ' ', description).strip()
        
        image = image_mapping.get(i, "")
        
        records.append({
            "id": i,
            "name": name,
            "region": region,
            "school": school,
            "title": title,
            "audience": audience,
            "subjects": subjects,
            "description": description,
            "project_link": primary_link,
            "image": image
        })

# Write js data file
js_content = f"const projectsData = {json.dumps(records, ensure_ascii=False, indent=2)};"
with open('projects-data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Generated projects-data.js with {len(records)} entries.")
