import json
import re


def process_single_value_links(entry: str) -> str:
    result_string = entry
    regex_string = "{@(\S+) ([^}]+)}"

    results = re.findall(regex_string, entry)
    for result in results:
        if "|" in result[1]:
            result_string = result[1].split("|")[0]
        result_string = result_string.replace(
            f"{{@{result[0]} {result[1]}}}", result[1]
        )

    return result_string


def process_multiple_value_links(entry: str) -> str:
    result_string = entry
    regex_string = "{@(\S+) ([^|]+)\|([^}]+)}"

    results = re.findall(regex_string, entry)
    for result in results:
        result_string = result_string.replace(
            f"{{@{result[0]} {result[1]}|{result[2]}}}", result[1]
        )

    return result_string


def get_spell_cost_by_level(level: int):
    match level:
        case None:
            return 0
        case 0:
            return 1500
        case 1:
            return 2500
        case 2:
            return 15000
        case 3:
            return 40000
        case 4:
            return 80000
        case 5:
            return 150000
        case 6:
            return 200000
        case 7:
            return 350000
        case 8:
            return 500000
        case 9:
            return 2000000


def process_entry_string(entry: str) -> str:
    return process_multiple_value_links(process_single_value_links(entry))


def get_desc_from_entries(entries: dict) -> str:
    # Some entries can be either a list of strings, or a list of dicts
    # Only return the strings
    description: str = ""

    for entry in entries:
        if isinstance(entry, str):
            description += f"{process_entry_string(entry)}\n"
    return description


def get_col_indices_for_name_and_price(column_labels):
    name_column = (
        1  # For now, this seems to just work as the name is always the second column
    )
    cost_column = None

    for index, column_label in enumerate(column_labels):
        if column_label == "SUGGESTED COST":
            cost_column = index

    if cost_column is None or name_column is None:
        print("Failed to determine name and cost columns in discerning merchants guide")
        exit(1)
    return name_column, cost_column


def get_item_price_by_name(name: str) -> int:
    return item_costs.get(name, 0)


item_costs = {}

with open("discerning-merchant-guide.json", "r") as fh:
    data = json.load(fh)

tables = data["table"]

for table in tables:
    name_column, cost_column = get_col_indices_for_name_and_price(table["colLabels"])
    # Iterate over each row in the table
    for row in table["rows"]:
        item_name = process_single_value_links(row[name_column])
        try:
            item_cost = (
                int(row[cost_column].split(" ")[0].replace(",", "")) * 100
            )  # Get cost, split at space, multiply by 100 for converting to number of copper
            item_costs[item_name] = item_cost
        except IndexError:
            print(f"Unable to get cost for {table['name']}")
        except ValueError:
            print(f"Unable to get cost for {table['name']}: invalid cost entry")

internal_books = {}

all_books = []
current_pk = 1

with open("books.json", "r") as fh:
    data = json.load(fh)

for book in data["book"]:
    all_books.append(
        {
            "model": "gen.book",
            "pk": current_pk,
            "fields": {
                "full_name": book["name"],
                "system": 1,
                "abbreviation": book["source"],
            },
        }
    )
    internal_books[book["source"]] = current_pk
    current_pk += 1

with open("adventures.json", "r") as fh:
    data = json.load(fh)

for adventure in data["adventure"]:
    all_books.append(
        {
            "model": "gen.book",
            "pk": current_pk,
            "fields": {
                "full_name": adventure["name"],
                "system": 1,
                "abbreviation": adventure["id"],
            },
        }
    )
    internal_books[adventure["id"]] = current_pk
    current_pk += 1

# Add manual book data since 5e tools doesn't have all of them
for manual_book in [
    ("TftYP", "Tales from the Yawning Portal"),
    ("RoTOS", "RoTOS"),
    ("EET", "Essentials Tome"),
    ("MCV2DC", "MVCV2DC"),
    ("HAT-LMI", "HAT-LMI"),
]:
    all_books.append(
        {
            "model": "gen.book",
            "pk": current_pk,
            "fields": {
                "full_name": manual_book[1],
                "system": 1,
                "abbreviation": manual_book[0],
            },
        }
    )
    internal_books[manual_book[0]] = current_pk
    current_pk += 1


# Serializing json
json_object = json.dumps(all_books, indent=4)

# Writing to fixtures.json
with open("../shop_gen/fixtures/books.json", "w") as outfile:
    outfile.write(json_object)

print("Processed books")

all_items = []
current_pk = 1

with open("items.json") as fh:
    data = json.load(fh)

types = set()

for item in data["item"]:

    item_price = item["value"] if "value" in item.keys() else 0
    if item_price == 0:
        item_price = get_item_price_by_name(item["name"])

    all_items.append(
        {
            "model": "gen.item",
            "pk": current_pk,
            "fields": {
                "name": item["name"],
                "description": (
                    get_desc_from_entries(item["entries"])
                    if "entries" in item.keys()
                    else ""
                ),
                "system": 1,
                "public": True,
                "price": (
                    item_price if item_price is not None else 0
                ),  # Because sometimes the item value is none
                "rarity": (
                    str(item["rarity"][0]).upper() if "rarity" in item.keys() else None
                ),
                "owner": 1,
                "sourcebook": (
                    internal_books[item["source"]]
                    if item["source"] in internal_books.keys()
                    else None
                ),
                "magical": (
                    True if "wondrous" in item.keys() and item["wondrous"] else False
                ),
                "type": item["type"] if "type" in item.keys() else None,
            },
        }
    )
    current_pk += 1

# Serializing json
json_object = json.dumps(all_items, indent=4)

# Writing to fixtures.json
with open("../shop_gen/fixtures/items.json", "w") as outfile:
    outfile.write(json_object)

print("Processed items")

all_spells = []
current_pk = 1

# with open("spells.json") as fh:
#     data = json.load(fh)
#
# for spell in data["spells"]:
#
#     level = spell["level"] if "level" in spell.keys() else None
#
#     all_spells.append(
#         {
#             "model": "gen.spell",
#             "pk": current_pk,
#             "fields": {
#                 "name": spell["name"],
#                 "description": (
#                     get_desc_from_entries(spell["entries"])
#                     if "entries" in spell.keys()
#                     else ""
#                 ),
#                 "sourcebook": (
#                     internal_books[spell["source"]]
#                     if spell["source"] in internal_books.keys()
#                     else None
#                 ),
#                 "system": 1,
#                 "public": True,
#                 "price": get_spell_cost_by_level(level),
#                 "level": level,
#                 "owner": 1,
#             },
#         }
#     )
#     current_pk += 1
#
# # Serializing json
# json_object = json.dumps(all_spells, indent=4)
#
# # Writing to fixtures.json
# with open("../shop_gen/fixtures/spells.json", "w") as outfile:
#     outfile.write(json_object)
#
# print("Processed spells")
