#!/bin/bash

# Define the folder path
folder_path="label_txts/"

# Check if the folder exists
if [ -d "$folder_path" ]; then
    # Delete all files and subdirectories in the folder
    rm -r "$folder_path"/*
    echo "All files and subdirectories in $folder_path have been deleted."
else
    echo "Folder $folder_path does not exist."
fi
