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
                if "is_published" == "TRUE":
                    row["is_published"] = True
                else:
                    row["is_published"] = False
            result.append({"model": model, "fields": row})

    with open(json_file, "w", encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False))


convert_file("categories.csv", "categories.json", "ads.category")
convert_file("ads.csv", "ads.json", "ads.ad")
