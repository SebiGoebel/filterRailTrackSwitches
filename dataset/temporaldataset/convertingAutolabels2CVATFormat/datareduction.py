"""
import os
import json

def filter_list_by_step_reverse(original_list, stepsize):
    new_list = []
    # Startindex ist das letzte Element der originalen Liste
    index = len(original_list) - 1
    
    # Solange der Index gültig ist (größer oder gleich 0)
    while index >= 0:
        new_list.append(original_list[index])  # Element zur neuen Liste hinzufügen
        index -= stepsize  # Index um die Schrittgröße reduzieren
    
    # Die neue Liste muss umgedreht werden, da wir rückwärts durchlaufen
    #new_list.reverse()
    return new_list

def read_and_print_json(file_path, output_folder):
    try:
        # JSON aus der Datei einlesen
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Daten auf der Konsole ausgeben
        #print(json.dumps(data, indent=2))  # JSON formatiert ausgeben

        # Extrahiere die Daten aus dem JSON
        sequence_name = list(data.keys())[0]  # "sequnce_55_frame_001345.png"
        left_rail = data[sequence_name]['left_rail']
        right_rail = data[sequence_name]['right_rail']

        reduced_left_rail = filter_list_by_step_reverse(left_rail, 5)
        reduced_right_rail = filter_list_by_step_reverse(right_rail, 5)

        data[sequence_name]['left_rail'] = reduced_left_rail
        data[sequence_name]['right_rail'] = reduced_right_rail
        
        # Dateinamen aus dem Eingabepfad extrahieren
        file_name = os.path.basename(file_path)
        
        # Sicherstellen, dass der Ausgabeordner existiert, falls nicht, erstellen
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"Ausgabeordner '{output_folder}' wurde erstellt.")
        
        # Ausgabepfad für die neue Datei erstellen
        output_file = os.path.join(output_folder, file_name)
        
        # JSON in die Ausgabedatei schreiben
        with open(output_file, 'w') as f:
            #json.dump(data, f, indent=2)
            json.dump(data, f, separators=(', ', ': '))
            print(f"JSON wurde in die Datei '{output_file}' geschrieben.")
            
    except FileNotFoundError:
        print(f"Die Datei '{file_path}' wurde nicht gefunden.")
    except json.JSONDecodeError as e:
        print(f"Fehler beim Decodieren der JSON-Datei '{file_path}': {e}")

if __name__ == "__main__":
    json_file = "tempData_Austria_Salzburg_Villach_jsons/sequnce_55_frame_001345.json"  # Hier den Pfad zur JSON-Datei angeben
    output_folder = "tempData_Austria_Salzburg_Villach_jsons_datareduction"  # Hier den Pfad zum Ausgabeordner angeben
    
    read_and_print_json(json_file, output_folder)
"""




import os
import json

def filter_list_by_step_reverse(original_list, stepsize):
    new_list = []
    index = len(original_list) - 1
    
    while index >= 0:
        new_list.append(original_list[index])
        index -= stepsize
    
    return new_list

def read_and_print_json(file_path, output_folder):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        sequence_name = list(data.keys())[0]
        left_rail = data[sequence_name]['left_rail']
        right_rail = data[sequence_name]['right_rail']

        data[sequence_name]['left_rail'] = filter_list_by_step_reverse(left_rail, 5)
        data[sequence_name]['right_rail'] = filter_list_by_step_reverse(right_rail, 5)
        
        file_name = os.path.basename(file_path)
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"Ausgabeordner '{output_folder}' wurde erstellt.")
        
        output_file = os.path.join(output_folder, file_name)
        
        with open(output_file, 'w') as f:
            json.dump(data, f, separators=(',', ':'))
            print(f"JSON wurde in die Datei '{output_file}' geschrieben.")
            
    except FileNotFoundError:
        print(f"Die Datei '{file_path}' wurde nicht gefunden.")
    except json.JSONDecodeError as e:
        print(f"Fehler beim Decodieren der JSON-Datei '{file_path}': {e}")

def process_folder(input_folder, output_folder):
    try:
        # Sicherstellen, dass der Ausgabeordner existiert, falls nicht, erstellen
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"Ausgabeordner '{output_folder}' wurde erstellt.")
        
        # Durchlaufe alle Dateien im Eingabeordner
        for filename in os.listdir(input_folder):
            if filename.endswith(".json"):
                file_path = os.path.join(input_folder, filename)
                read_and_print_json(file_path, output_folder)
    
    except FileNotFoundError:
        print(f"Der Ordner '{input_folder}' wurde nicht gefunden.")

if __name__ == "__main__":
    input_folder = "tempData_Austria_Salzburg_Villach_jsons"
    output_folder = "tempData_Austria_Salzburg_Villach_jsons_datareduction"
    
    process_folder(input_folder, output_folder)
