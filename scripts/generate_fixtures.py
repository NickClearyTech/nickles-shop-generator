import json


def get_desc_from_entries(entries: dict) -> str:
    # Some entries can be either a list of strings, or a list of dicts
    # Only return the strings
    description: str = ""

    for entry in entries:
        if isinstance(entry, str):
            description += f"{entry}\n"
    return description


all_items = []
current_pk = 1

with open("items.json") as fh:
    data = json.load(fh)

for item in data["item"]:
    all_items.append(
        {
            "model": "gen.item",
            "pk": current_pk,
            "fields": {
                "name": item["name"],
                "description": get_desc_from_entries(item["entries"]) if "entries" in item.keys() else "",
                "system": 1,
                "public": True,
                "price": 0,
                "rarity": str(item["rarity"][0]).upper() if "rarity" in item.keys() else None
            }
        }
    )
    current_pk += 1

# Serializing json
json_object = json.dumps(all_items, indent=4)

# Writing to fixtures.json
with open("../shop_gen/fixtures.json", "w") as outfile:
    outfile.write(json_object)
