import json

def extract_paths(data):
    def extract_name_from_list(name_list):
        return name_list[0]["#text"] if name_list else ""

    def recurse(concept, path):
        name = extract_name_from_list(concept.get("name", []))
        new_path = path + [name]
        if "concept" in concept:
            return sum([recurse(sub_concept, new_path) for sub_concept in concept["concept"]], [])
        else:
            return [new_path]

    paths = []
    for dataset in data.get("dataset", []):
        dataset_name = extract_name_from_list(dataset.get("name", []))
        for concept in dataset.get("concept", []):
            paths.extend(recurse(concept, [dataset_name]))

    return paths


data = json.load(open("raw_art_decor/fullArtDecor.json"))

paths = extract_paths(data)

for path in paths:
    print(".".join(path))