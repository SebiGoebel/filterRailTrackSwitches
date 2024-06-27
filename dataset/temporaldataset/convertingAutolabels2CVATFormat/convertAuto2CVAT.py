import os
import json
from datumaro.components.project import Project
from datumaro.components.dataset import Dataset, DatasetItem
from datumaro.components.annotation import PolyLine, LabelCategories, AnnotationType
from datumaro.util.image import Image

def convert_to_datumaro(input_folder, output_folder):
    # Erstelle ein neues Datumaro-Projekt
    project = Project()

    # Definiere die Label-Kategorien
    labels = ['left_rail', 'right_rail']
    label_cat = LabelCategories()
    for label in labels:
        label_cat.add(label)
    categories = {AnnotationType.label: label_cat}

    # Erstelle ein neues Dataset
    dataset = Dataset(categories=categories)

    # Durchlaufe alle JSON-Dateien im Eingabeordner
    for json_file in os.listdir(input_folder):
        if json_file.endswith('.json'):
            with open(os.path.join(input_folder, json_file), 'r') as f:
                annotations = json.load(f)

            for image_name, objects in annotations.items():
                image_path = os.path.join(input_folder, image_name)
                if not os.path.exists(image_path):
                    continue

                polyline_annotations = []
                for label, points in objects.items():
                    points = [(float(x), float(y)) for x, y in points]
                    polyline_annotations.append(PolyLine(points, label=labels.index(label)))

                dataset.add(DatasetItem(
                    id=image_name,
                    image=Image(path=image_path),
                    annotations=polyline_annotations
                ))

    # Speichere das Dataset im Datumaro-Format
    dataset.export(output_folder, 'datumaro', save_images=True)
    print(f"Dataset erfolgreich im Datumaro-Format in '{output_folder}' gespeichert.")

# Verwendet das Skript
input_folder = 'tempData_Austria_Salzburg_Villach_jsons'
output_folder = 'datumaro_dataset'
convert_to_datumaro(input_folder, output_folder)
