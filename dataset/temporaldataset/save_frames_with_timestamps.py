import cv2
import os

def save_frames_from_video(timestamps_file, output_folder, frames_offset=75):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Read the video filename from the timestamps file
    with open(timestamps_file, 'r') as file:
        lines = file.readlines()
        video_filename = lines[0].strip()
        timestamps = [int(line.strip()) for line in lines[1:]]
    
    video_capture = cv2.VideoCapture(video_filename) # Open the video file

    # Check if video opened successfully
    if not video_capture.isOpened():
        print(f"Error: Could not open video {video_filename}.")
        return

    fps = video_capture.get(cv2.CAP_PROP_FPS) # Get frames per second (fps) of the video
    
    # Calculate the frame numbers to extract based on the timestamps
    frame_numbers_dict = {}
    for timestamp in timestamps:
        frame_number = int(timestamp * fps)
        frame_numbers_dict[timestamp] = [frame_number + offset for offset in range(-frames_offset, frames_offset + 1)]
    
    # Extract and save the frames
    frame_index = 0
    all_frame_numbers = sorted(set(num for sublist in frame_numbers_dict.values() for num in sublist))
    frame_number_set = set(all_frame_numbers)

    while True:
        # Read the next frame from the video
        success, frame = video_capture.read()

        # Break the loop if there are no more frames
        if not success: 
            break

        if frame_index in frame_number_set:
            # Determine which sequence this frame belongs to
            for sequence_index, frame_numbers in frame_numbers_dict.items():
                if frame_index in frame_numbers:
                    # Save the frame as an image file
                    frame_filename = os.path.join(output_folder, f"sequnce_{sequence_index}_frame_{frame_index:06d}.png")
                    cv2.imwrite(frame_filename, frame)
                    
                    # Print frame information
                    print(f"Saved {frame_filename}")

        frame_index += 1

    # Release the video capture object
    video_capture.release()
    print("Done saving frames.")

# Example usage
timestamps_file = 'weichenSekunden_Austria_Salzburg_Villach.txt'
output_folder = 'tempData_Austria_Salzburg_Villach'
save_frames_from_video(timestamps_file, output_folder)
