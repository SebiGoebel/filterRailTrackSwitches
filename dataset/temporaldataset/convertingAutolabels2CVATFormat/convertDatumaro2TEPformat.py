
"""
This file converts the Datuaro_v1.0 format into the TEP formt.
it takes a .json file as input and also outputs a .json file
"""

import json
import os

# Pfad zur Eingabe-JSON-Datei
input_json_file_path = '/home/sebi/filterRailTrackSwitches/dataset/temporaldataset/temporalSwitchDataset_DatumaroFormat/annotations/default.json'
# Pfad zur Ausgabe-JSON-Datei
output_json_file_path = 'output.json'

# JSON-Datei einlesen
with open(input_json_file_path, 'r') as file:
    data = json.load(file)

# Label-Namen aus dem Info-Block zuordnen
label_mapping = {i: label['name'] for i, label in enumerate(data['categories']['label']['labels'])}

# Neues Datenformat erstellen
output_data = {}

# Durch die Items iterieren und die Bildnamen, Label und Polylinienpunkte hinzufügen
for item in data['items']:
    # Bildnamen anpassen
    image_id = os.path.splitext(os.path.basename(item['id']))[0] + '.png'
    output_data[image_id] = {}
    for annotation in item['annotations']:
        if annotation['type'] == 'polyline':
            label = label_mapping.get(annotation['label_id'], 'unknown')
            if label not in output_data[image_id]:
                output_data[image_id][label] = []
            rounded_points = [[round(point) for point in annotation['points'][i:i+2]] for i in range(0, len(annotation['points']), 2)]
            output_data[image_id][label].extend(rounded_points)

# Ausgabe-JSON-Datei speichern, alles in einer Zeile
with open(output_json_file_path, 'w') as outfile:
    json.dump(output_data, outfile, separators=(', ', ': '))

print(f"Data has been successfully written to {output_json_file_path}")
