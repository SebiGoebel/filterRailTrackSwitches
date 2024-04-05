import json

"""
This script converts the label-format of RailSem19 into the label-format of DarkNet which is usually used by yolos.
Examples of this formats are provided in the following.

RailSem19 format:

{
    "frame": "rs00000", 
    "imgHeight": 1080, 
    "imgWidth": 1920, 
    "objects": [
        {
            "boundingbox": [
                1066, 
                571, 
                1077, 
                590
            ], 
            "label": "track-sign-front"
        }, 
        {
            "boundingbox": [
                1024, 
                599, 
                1052, 
                612
            ], 
            "label": "switch-unknown"
        },  
        {
            "label": "pole", 
            "polygon": [
                [
                    1084, 
                    527
                ],
                ...
                [
                    1084, 
                    520
                ]
            ]
        },  
        {
            "label": "pole", 
            "polygon": [
                [
                    1125, 
                    535
                ], 
                ... 
                [
                    1128, 
                    534
                ]
            ]
        },
    ]
}

DarkNet format:

the format of each row:
class_id center_x center_y width height

img0001.txt:
1 0.408 0.30266666666666664 0.104 0.15733333333333333
1 0.245 0.424 0.046 0.08

darknet.labels:
head
helmet
person

"""

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

    print("--------------- Bounding Boxes with Labels: ---------------")

    for bounding_box in bounding_boxes_with_labels:
        print("Label:", bounding_box['label'])
        print("Bounding Box:", bounding_box['boundingbox'])

    print("--------------- Bounding Boxes with Labels with counter: ---------------")

    for i, bounding_box in enumerate(bounding_boxes_with_labels, start=1):
        print(f"Bounding Box {i}:")
        print("Label:", bounding_box['label'])
        print("Bounding Box:", bounding_box['boundingbox'])

    # Print the total number of bounding boxes
    print(f"Total Bounding Boxes: {len(bounding_boxes_with_labels)}")
