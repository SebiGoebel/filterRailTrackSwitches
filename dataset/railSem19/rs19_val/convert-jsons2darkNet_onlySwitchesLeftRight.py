import json
import os

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

# counters for each label
error_counter = 0
track_sign_front_counter = 0
track_signal_front_counter = 0
track_signal_back_counter = 0
crossing_counter = 0
switch_unknown_counter = 0
switch_left_counter = 0
switch_indicator_counter = 0
switch_static_counter = 0
switch_right_counter = 0
buffer_stop_counter = 0

write_label_counter = 0

# reading from json
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# writing labels to txt (darknet.labls)
def write_labels_to_file_darknet(list, file_path):
    with open(file_path, 'w') as file:
        for index, item in enumerate(list):
            file.write(str(item))
            if index != len(list) - 1: # after last label no '\n'
                file.write('\n')

# writing lables to txt (frame.txt)
def write_multiple_labels_to_file(labels, file_path):
    with open(file_path, 'w') as file:
        for i, line_labels in enumerate(labels):
            line = ' '.join(map(str, line_labels))
            if i < len(labels) - 1:  # after last label no '\n'
                file.write(line + '\n')
            else:
                file.write(line)

# check and update label list
def check_and_update_label_list(label, label_list):
    if label in label_list:
        return label_list.index(label)
    else:
        label_list.append(label)
        return len(label_list) - 1

# converting bounding box parameters form railSem19-format to darkNet-format
def converting_bounding_boxes_parameters(current_label, current_bounding_box, imgWidth, imgHeight):
    # first assumption: points of bounding_box is top-left and bottom-right
    top_left_x = current_bounding_box[0]
    top_left_y = current_bounding_box[1]
    bottom_right_x = current_bounding_box[2]
    bottom_right_y = current_bounding_box[3]
    
    # calculating new parameters of bounding boxes
    x_centre = (top_left_x + (bottom_right_x - top_left_x) / 2) / imgWidth
    y_centre = (top_left_y + (bottom_right_y - top_left_y) / 2) / imgHeight
    w_rel = (bottom_right_x - top_left_x) / imgWidth
    h_rel = (bottom_right_y - top_left_y) / imgHeight
    
    # writing numbers to .txt file
    label_number = check_and_update_label_list(current_label, label_list) # converting label from string to number
    new_bounding_box = [label_number, x_centre, y_centre, w_rel, h_rel]
    return new_bounding_box

# increasing check-counters for each label
def counting_labels(label):
    if label == "crossing":
        global crossing_counter
        crossing_counter += 1
    elif label == "track-signal-back":
        global track_signal_back_counter
        track_signal_back_counter += 1
    elif label == "track-signal-front":
        global track_signal_front_counter
        track_signal_front_counter +=1
    elif label == "track-sign-front":
        global track_sign_front_counter
        track_sign_front_counter += 1
    elif label == "switch-unknown":
        global switch_unknown_counter
        switch_unknown_counter += 1
    elif label == "switch-left":
        global switch_left_counter
        switch_left_counter += 1
    elif label == "switch-indicator":
        global switch_indicator_counter
        switch_indicator_counter += 1
    elif label == "switch-static":
        global switch_static_counter
        switch_static_counter += 1
    elif label == "switch-right":
        global switch_right_counter
        switch_right_counter += 1
    elif label == "buffer-stop":
        global buffer_stop_counter
        buffer_stop_counter += 1
    else:
        global error_counter
        error_counter += 1  # no label fits

def converting_single_json(json_file_path, write_folder_path, darknet_filename):
    # reading from single json file
    #json_file_path = read_folder_path + "rs" + str(json_number).zfill(5) + ".json"
    json_content = read_json_file(json_file_path)

    # Extract required parameters
    frame = json_content['frame']
    imgHeight = json_content['imgHeight']
    imgWidth = json_content['imgWidth']

    print("converting label data of frame: ", frame)

    # Extract boundingbox and label from objects
    bounding_boxes_with_labels = []
    for obj in json_content['objects']:
        if 'boundingbox' in obj and 'label' in obj:
            label = obj['label']
            bounding_box = obj['boundingbox']
            if label == "switch-unknown" or label == "switch-left" or label == "switch-right":
                global write_label_counter
                write_label_counter += 1
                bounding_boxes_with_labels.append({'label': label, 'boundingbox': bounding_box})

    all_labels_current_image = []

    # filtering out frames that include "switch-unknown"-labels
    for bounding_box in bounding_boxes_with_labels:
        if bounding_box['label'] == "switch-unknown":
            bounding_boxes_with_labels.clear()
            break

    # convertion of label-data
    for bounding_box in bounding_boxes_with_labels:
        current_label = bounding_box['label']
        current_bounding_box = bounding_box['boundingbox']
        counting_labels(current_label)                                                                                    # counting labels for control purposes
        new_bounding_box = converting_bounding_boxes_parameters(current_label, current_bounding_box, imgWidth, imgHeight) # converting parameters
        all_labels_current_image.append(new_bounding_box)                                                                 # add parameters [label_number, x_centre, y_centre, width, height] to all_labels list

    # writing converted labels to .txt file
    write_file_path = write_folder_path + frame + ".txt"
    write_multiple_labels_to_file(all_labels_current_image, write_file_path)

    # writing labels to darknet.label file
    if all_labels_current_image: # check if list is empty
        write_darknet_path = write_folder_path + darknet_filename
        write_labels_to_file_darknet(label_list, write_darknet_path)

if __name__ == "__main__":
    # paths for read and write folders and files
    read_folder_path = "jsons/rs19_val/"
    #read_folder_path = "jsons/test/"
    write_folder_path = "darknets/onlyFramesWithSwitchesLeftRight/"
    darknet_filename = "darknet.labels"

    label_list = [] # for all different labels -> darknet.label

    # iterate through whole folder
    for filename in os.listdir(read_folder_path):
        file_path = os.path.join(read_folder_path, filename)
        if os.path.isfile(file_path):
            converting_single_json(file_path, write_folder_path, darknet_filename)

    print("==========================================================")
    print("track_sign_front_counter: ", track_sign_front_counter)
    print("track_signal_front_counter: ", track_signal_front_counter)
    print("track_signal_back_counter: ", track_signal_back_counter)
    print("crossing_counter: ", crossing_counter)
    print("switch_unknown_counter: ", switch_unknown_counter)
    print("switch_left_counter: ", switch_left_counter)
    print("switch_indicator_counter: ", switch_indicator_counter)
    print("switch_static_counter: ", switch_static_counter)
    print("switch_right_counter: ", switch_right_counter)
    print("buffer_stop_counter: ", buffer_stop_counter)
    print("error_counter: ", error_counter)
    print("----------------------------------------------------------")
    print("write_label_counter: ", write_label_counter)
