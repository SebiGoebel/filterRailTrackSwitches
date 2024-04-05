import json

def read_json_file(file_path):
    """Read JSON file and return its content."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

if __name__ == "__main__":
    file_path = input("Enter the path to the JSON file: ")
    json_content = read_json_file(file_path)
    
    # Extract required fields
    frame = json_content['frame']
    imgHeight = json_content['imgHeight']
    imgWidth = json_content['imgWidth']
    
    # Extract boundingbox and label from objects
    bounding_boxes_with_labels = []
    for obj in json_content['objects']:
        if 'boundingbox' in obj and 'label' in obj:
            label = obj['label']
            bounding_box = obj['boundingbox']
            bounding_boxes_with_labels.append({'label': label, 'boundingbox': bounding_box})

    # Print the extracted fields
    print("frame:", frame)
    print("imgHeight:", imgHeight)
    print("imgWidth:", imgWidth)
    print("Bounding Boxes with Labels:")
    for bounding_box in bounding_boxes_with_labels:
        print("Label:", bounding_box['label'])
        print("Bounding Box:", bounding_box['boundingbox'])
