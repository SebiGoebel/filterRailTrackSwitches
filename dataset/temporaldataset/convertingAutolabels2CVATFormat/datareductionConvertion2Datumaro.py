import os
import json

def filter_list_by_step_reverse(original_list, stepsize):
    new_list = []
    index = len(original_list) - 1
    
    while index >= 0:
        new_list.append(original_list[index])
        index -= stepsize
    
    return new_list

def read_json(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        sequence_name = list(data.keys())[0]
        left_rail = data[sequence_name]['left_rail']
        right_rail = data[sequence_name]['right_rail']

        data[sequence_name]['left_rail'] = filter_list_by_step_reverse(left_rail, 5)
        data[sequence_name]['right_rail'] = filter_list_by_step_reverse(right_rail, 5)
        
        return data
    
    except FileNotFoundError:
        print(f"Die Datei '{file_path}' wurde nicht gefunden.")
        return None
    except json.JSONDecodeError as e:
        print(f"Fehler beim Decodieren der JSON-Datei '{file_path}': {e}")
        return None

def process_folder(input_folder, output_file):
    combined_data = {
        "info": {},
        "categories": {
            "label": {
                "labels": [
                    {"name": "left_rail", "parent": "", "attributes": []},
                    {"name": "right_rail", "parent": "", "attributes": []}
                ],
                "attributes": []
            }
        },
        "items": []
    }
    annotation_id = 0
    
    try:
        # Sicherstellen, dass der Eingabeordner existiert
        if not os.path.exists(input_folder):
            print(f"Der Ordner '{input_folder}' wurde nicht gefunden.")
            return
        
        # Durchlaufe alle Dateien im Eingabeordner
        for filename in os.listdir(input_folder):
            if filename.endswith(".json"):
                file_path = os.path.join(input_folder, filename)
                data = read_json(file_path)
                if data:
                    sequence_name = list(data.keys())[0]
                    item = {
                        "id": sequence_name,
                        "annotations": []
                    }
                    
                    left_rail_points = [coord for point in data[sequence_name]['left_rail'] for coord in point]
                    right_rail_points = [coord for point in data[sequence_name]['right_rail'] for coord in point]
                    
                    item['annotations'].append({
                        "id": annotation_id,
                        "type": "polyline",
                        "attributes": {},
                        "group": 0,
                        "label_id": 0,
                        "points": left_rail_points,
                        "z_order": 0
                    })
                    annotation_id += 1
                    
                    item['annotations'].append({
                        "id": annotation_id,
                        "type": "polyline",
                        "attributes": {},
                        "group": 1,
                        "label_id": 1,
                        "points": right_rail_points,
                        "z_order": 0
                    })
                    annotation_id += 1
                    
                    combined_data['items'].append(item)
        
        # Sicherstellen, dass der Ausgabeordner existiert, falls nicht, erstellen
        output_folder = os.path.dirname(output_file)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"Ausgabeordner '{output_folder}' wurde erstellt.")
        
        # JSON in die Ausgabedatei schreiben
        with open(output_file, 'w') as f:
            json.dump(combined_data, f, indent=4)
            print(f"Alle JSON-Daten wurden in die Datei '{output_file}' geschrieben.")
    
    except FileNotFoundError:
        print(f"Der Ordner '{input_folder}' wurde nicht gefunden.")

if __name__ == "__main__":
    current_directory = os.getcwd()
    print(f"Aktuelles Arbeitsverzeichnis: {current_directory}")
    
    input_folder = "tempData_Austria_Salzburg_Villach_jsons"
    output_file = "annotations/default.json"
    
    process_folder(input_folder, output_file)
