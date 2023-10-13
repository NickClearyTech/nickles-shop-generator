import json

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
                "description": "\n".join(item["entries"]) if "entries" in item.keys() else "",
                "system": 1,
                "public": True,
                "price": 0,
                "rarity": str(item["rarity"][0]).upper() if "rarity" in item.keys() else None
            }
        }
    )