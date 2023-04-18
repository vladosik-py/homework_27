import csv
import json


def convert_file(csv_file, json_file, model):
    result = []
    with open(csv_file, encoding='utf-8') as csv_f:
        for row in csv.DictReader(csv_f):
            del row["id"]
            if "price" in row:
                row["price"] = int(row["price"])

            if "is_published" in row:
                if row["is_published"] == "TRUE":
                    row["is_published"] = True
                else:
                    row["is_published"] = False

            if "location_id" in row:
                row["location"] = [row["location_id"]]
                del row["location_id"]

            result.append({"model": model, "fields": row})


    with open(json_file, "w", encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False))


convert_file("data_28/category.csv", "data_28/category.json", "ads.category")
convert_file("data_28/ad.csv", "data_28/ad.json", "ads.ad")

convert_file("data_28/user.csv", "data_28/user.json", "users.user")
convert_file("data_28/location.csv", "data_28/location.json", "users.location")