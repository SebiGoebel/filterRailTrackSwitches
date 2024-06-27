import os
import json
from datumaro.components.dataset import Dataset, DatasetItem
from datumaro.components.annotation import PolyLine, LabelCategories, AnnotationType
from datumaro.util.image import Image

class CustomExtractor:
    def __init__(self, images_dir):
        self._items = []
        self._categories = {
            AnnotationType.label: LabelCategories.from_iterable(['left_rail', 'right_rail'])
        }
        self._load_annotations(images_dir)

    def _load_annotations(self, images_dir):
        annotation_files = [f for f in os.listdir(images_dir) if f.endswith('.json')]
        print(f"Gefundene Annotationsdateien: {annotation_files}")

        for annotation_file in annotation_files:
            annotation_path = os.path.join(images_dir, annotation_file)
            with open(annotation_path, 'r') as f:
                annotations = json.load(f)
            print(f"Lade Annotations aus {annotation_path}")

            for image_name, objects in annotations.items():
                image_path = os.path.join(images_dir, image_name)
                if not os.path.exists(image_path):
                    print(f"Bild {image_path} existiert nicht, überspringe.")
                    continue

                polyline_annotations = []
                for label, points in objects.items():
                    points = [(float(x), float(y)) for x, y in points]
                    polyline_annotations.append(PolyLine(points, label=self._categories[AnnotationType.label].find(label)[0]))

                self._items.append(DatasetItem(
                    id=image_name,
                    media=Image(path=image_path),
                    annotations=polyline_annotations
                ))
                print(f"Füge DatasetItem für {image_name} hinzu mit {len(polyline_annotations)} Annotationen.")

    def __iter__(self):
        return iter(self._items)

    def categories(self):
        return self._categories

def convert_to_datumaro(input_folder, output_folder):
    extractor = CustomExtractor(input_folder)
    dataset = Dataset.from_extractors(extractor)

    # Speichere das Dataset im Datumaro-Format
    dataset.export(output_folder, 'datumaro', save_media=True)
    print(f"Dataset erfolgreich im Datumaro-Format in '{output_folder}' gespeichert.")

# Verwendet das Skript
input_folder = 'tempData_Austria_Salzburg_Villach_jsons'
output_folder = 'datumaro_dataset'
convert_to_datumaro(input_folder, output_folder)
