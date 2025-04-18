import csv
import requests

def get_gender_from_wikidata(name):
    try:
        # Step 1: Search for the entity in Wikidata
        search_url = "https://www.wikidata.org/w/api.php"
        params = {
            'action': 'wbsearchentities',
            'format': 'json',
            'language': 'en',
            'search': name
        }
        res = requests.get(search_url, params=params).json()
        
        if not res['search']:
            return "Not found"

        qid = res['search'][0]['id']  # First matched entity, usually accurate

        # Step 2: Get entity data
        entity_url = f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
        entity_data = requests.get(entity_url).json()
        
        claims = entity_data['entities'][qid]['claims']
        gender_claim = claims.get('P21')
        if not gender_claim:
            return "Unknown"
        
        # Step 3: Get the label of the gender
        gender_id = gender_claim[0]['mainsnak']['datavalue']['value']['id']
        
        # Step 4: Convert gender Q-ID to label (like Q6581097 → 'male')
        label_url = f"https://www.wikidata.org/wiki/Special:EntityData/{gender_id}.json"
        gender_data = requests.get(label_url).json()
        gender_label = gender_data['entities'][gender_id]['labels']['en']['value']
        
        return gender_label

    except Exception as e:
        return f"Error: {e}"

# ---- CSV I/O ---- #
input_csv = "albums_genres_grouped.csv"
output_csv = "names_with_gender.csv"

results = []

with open(input_csv, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row['artist_name']
        gender = get_gender_from_wikidata(name)
        results.append({'name': name, 'gender': gender})
        print(f"{name} → {gender}")

with open(output_csv, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['name', 'gender'])
    writer.writeheader()
    writer.writerows(results)

print(f"\nSaved gender info to {output_csv}")

