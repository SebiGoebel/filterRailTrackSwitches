import json
import os
import shutil

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

# writing frames to txt (only_frames_with_switches.txt)
def write_list_to_file(listOfFrames, filename):
    with open(filename, 'w') as file:
        for frame in listOfFrames:
            file.write(frame + '\n')

# copy file from to
def copy_file(quell_pfad, ziel_pfad):
    json_file_path = read_jsons + "rs" + str(json_number).zfill(5) + ".json"
    try:
        shutil.copy(quell_pfad, ziel_pfad)
        print(f"Datei von {quell_pfad} nach {ziel_pfad} kopiert.")
    except IOError as e:
        print(f"Fehler beim Kopieren der Datei: {e}")
    except Exception as e:
        print(f"Unerwarteter Fehler: {e}")

if __name__ == "__main__":
    # ---------- paths for read and write folders and files ----------
    #jsons
    #read_jsons = "jsons/rs19_val/"
    read_jsons = "jsons/test/"
    write_jsons = "jsons/onylFramesWithSwitches_jsons/"
    #jpgs
    read_jpgs = "jpgs/rs19_val/"
    write_jpgs = "jpgs/onlyFramesWithSwitches_jpgs/"
    #uint8
    read_uint8 = "uint8/rs19_val/"
    write_uint8 = "uint8/onlyFramesWithSwitches_uint8/"
    #list of frames
    write_frames_list_txt = "list_of_frames_containing_switches.txt"
    # ----------------------------------------------------------------

    # counters for each label
    error_counter = 0
    frames_with_switches_counter = 0
    switch_unknown_counter = 0
    switch_left_counter = 0
    switch_indicator_counter = 0
    switch_static_counter = 0
    switch_right_counter = 0

    # unused label counters
    #track_sign_front_counter = 0
    #track_signal_front_counter = 0
    #track_signal_back_counter = 0
    #crossing_counter = 0
    #buffer_stop_counter = 0

    listOnlyFramesWithSwitches = []

    # iterate through whole folder
    for filename in os.listdir(read_jsons):
        file_path = os.path.join(read_jsons, filename)
        if os.path.isfile(file_path):
            print(file_path)
            json_content = read_json_file(file_path)

            # Extracting frame
            frame = json_content['frame']

            checker = False

            # Extract boundingbox and label from objects
            bounding_boxes_with_labels = []
            for obj in json_content['objects']:
                if 'boundingbox' in obj and 'label' in obj:
                    label = obj['label']
                    bounding_box = obj['boundingbox']
                    bounding_boxes_with_labels.append({'label': label, 'boundingbox': bounding_box})

            # increase corresponding counter for each label
            for bounding_box in bounding_boxes_with_labels:
                current_label = bounding_box['label']

                if current_label == "switch-unknown":
                    switch_unknown_counter += 1
                elif current_label == "switch-left":
                    switch_left_counter += 1
                elif current_label == "switch-indicator":
                    switch_indicator_counter += 1
                elif current_label == "switch-static":
                    switch_static_counter += 1
                elif current_label == "switch-right":
                    switch_right_counter += 1
                else:
                    error_counter += 1  # no label fits

                if not checker and (current_label == "switch-unknown" or current_label == "switch-left" or current_label == "switch-right"):
                    frames_with_switches_counter += 1
                    listOnlyFramesWithSwitches.append(frame)
                    checker = True
                
    print("==========================================================")

    print(listOnlyFramesWithSwitches)

    print("writing frames to txt ...")
    write_list_to_file(listOnlyFramesWithSwitches, write_frames_list_txt)

    print("==========================================================")
    print("frames_with_switches_counter: ", frames_with_switches_counter)
    print("switch_unknown_counter: ", switch_unknown_counter)
    print("switch_left_counter: ", switch_left_counter)
    print("switch_indicator_counter: ", switch_indicator_counter)
    print("switch_static_counter: ", switch_static_counter)
    print("switch_right_counter: ", switch_right_counter)
    print("error_counter: ", error_counter)
