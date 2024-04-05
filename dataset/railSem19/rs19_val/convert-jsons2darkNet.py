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

# reading from json
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# writing lables to txt
"""def write_labels_to_file(labels, file_path):
    with open(file_path, 'w') as file:
        line = ' '.join(map(str, labels))
        file.write(line)

def write_labels_to_file_append(labels, file_path):
    with open(file_path, 'a') as file:
        line = ' '.join(map(str, labels))
        file.write(line + '\n')
"""
# writing labels to txt (darknet.labls)
def write_labels_to_file_darknet(list, file_path):
    with open(file_path, 'w') as file:
        for index, item in enumerate(list):
            file.write(str(item))
            if index != len(list) - 1: # after last label no '\n'
                file.write('\n')

# writing lables to txt
def write_multiple_labels_to_file(labels, file_path):
    with open(file_path, 'w') as file:
        for i, line_labels in enumerate(labels):
            line = ' '.join(map(str, line_labels))
            if i < len(labels) - 1:  # after last label no '\n'
                file.write(line + '\n')
            else:
                file.write(line)

# converting bounding box parameters form railSem19-format to darkNet-format
def converting_bounding_boxes_parameters(current_bounding_box):
    print("current Box:", current_bounding_box)
    
    # first assumption: points of bounding_box is top-left and bottom-right
    top_left_x = current_bounding_box[0]
    top_left_y = current_bounding_box[1]
    bottom_right_x = current_bounding_box[2]
    bottom_right_y = current_bounding_box[3]
    
    print("-------------")
    
    print("top-left_x:", top_left_x)
    print("top-left_y:", top_left_y)
    print("bottom-right_x:", bottom_right_x)
    print("bottom-right_y:", bottom_right_y)
    
    # calculating new parameters of bounding boxes
    x_centre = (top_left_x + (bottom_right_x - top_left_x) / 2) / imgWidth
    y_centre = (top_left_y + (bottom_right_y - top_left_y) / 2) / imgHeight
    w_rel = (bottom_right_x - top_left_x) / imgWidth
    h_rel = (bottom_right_y - top_left_y) / imgHeight
    
    print("-------------")
    
    print("label:", current_label)
    print("x:", x_centre)
    print("y:", y_centre)
    print("w:", w_rel)
    print("h:", h_rel)

    print("===========")

    print("writing number to .txt file")
    new_bounding_box = [current_label, x_centre, y_centre, w_rel, h_rel]
    return new_bounding_box

# converting label from text to numbers
def converting_label_text2numbers(label):
    if label == "abc":
        return 1
    elif label == "klj":
        return 2
    elif label == "xyz":
        return 3
    elif label == "udf":
        return 4
    else:
        return 0  # 0 --> no label fits

# check and update label list
def check_and_update_label_list(label, label_list):
    if label in label_list:
        return label_list.index(label)
    else:
        label_list.append(label)
        return len(label_list) - 1

if __name__ == "__main__":
    #file_path = input("Enter the path to the JSON file: ") # input in terminal
    read_file_path = "jsons/rs19_val/rs00000.json"               # hardcoded for rs00000.json
    write_folder_path = "darknets/"
    txt_extension = ".txt"
    darknet_filename = "darknet.labels"

    write_darknet_path = write_folder_path + darknet_filename

    json_content = read_json_file(read_file_path)

    label_list = []
    
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

    print("--------------- Convertion of label data: ---------------")

    all_labels_current_image = []

    # convertion of label-data
    for bounding_box in bounding_boxes_with_labels:
        current_label = bounding_box['label']
        print("current Label:", current_label)
        check_and_update_label_list(current_label, label_list)

        current_bounding_box = bounding_box['boundingbox']
        new_bounding_box = converting_bounding_boxes_parameters(current_bounding_box)

        # add to all_labels list
        all_labels_current_image.append(new_bounding_box)

    print(all_labels_current_image)

    write_file_path = write_folder_path + frame + txt_extension

    write_multiple_labels_to_file(all_labels_current_image, write_file_path)

    print(label_list)
    write_labels_to_file_darknet(label_list, write_darknet_path)

