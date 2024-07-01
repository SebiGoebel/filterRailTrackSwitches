import os
import json

def process_items_to_old_format(items):
    old_format_data = {}
    for item in items:
        sequence_name = item['id']
        left_rail_points = []
        right_rail_points = []

        for annotation in item['annotations']:
            if annotation['type'] == 'polyline':
                if annotation['label_id'] == 0:
                    left_rail_points = [annotation['points'][i:i+2] for i in range(0, len(annotation['points']), 2)]
                elif annotation['label_id'] == 1:
                    right_rail_points = [annotation['points'][i:i+2] for i in range(0, len(annotation['points']), 2)]

        old_format_data[sequence_name] = {
            "left_rail": left_rail_points,
            "right_rail": right_rail_points
        }
    return old_format_data

def read_json(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"Die Datei '{file_path}' wurde nicht gefunden.")
        return None
    except json.JSONDecodeError as e:
        print(f"Fehler beim Decodieren der JSON-Datei '{file_path}': {e}")
        return None

def process_folder(input_file, output_folder):
    try:
        # Sicherstellen, dass die Eingabedatei existiert
        if not os.path.exists(input_file):
            print(f"Die Datei '{input_file}' wurde nicht gefunden.")
            return

        data = read_json(input_file)
        if data:
            items = data['items']
            old_format_data = process_items_to_old_format(items)

            # Sicherstellen, dass der Ausgabeordner existiert, falls nicht, erstellen
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
                print(f"Ausgabeordner '{output_folder}' wurde erstellt.")
            
            # JSON in die Ausgabedatei schreiben
            output_file = os.path.join(output_folder, "converted_data.json")
            with open(output_file, 'w') as f:
                json.dump(old_format_data, f, indent=4)
                print(f"Die konvertierten JSON-Daten wurden in die Datei '{output_file}' geschrieben.")

    except FileNotFoundError:
        print(f"Die Datei '{input_file}' wurde nicht gefunden.")

if __name__ == "__main__":
    current_directory = os.getcwd()
    print(f"Aktuelles Arbeitsverzeichnis: {current_directory}")
    
    input_file = "tempData_Austria_Salzburg_Villach_jsons_datareduction/combined_data.json"
    output_folder = "tempData_Austria_Salzburg_Villach_jsons_old_format"
    
    process_folder(input_file, output_folder)
