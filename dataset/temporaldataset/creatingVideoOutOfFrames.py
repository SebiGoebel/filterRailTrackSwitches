import cv2
import os

# Pfade festlegen
frames_folder = 'tempData_outputSingleFrameBased_long'  # Ordner, in dem die Frames gespeichert sind
output_folder = 'videos'  # Ordner, in dem das Video gespeichert werden soll
output_filename = 'temporalDataset_video_singleFrameBasedModel_prediction_long.mp4'  # Name der Ausgabedatei

# Erstellen des Ausgabeordners, falls nicht vorhanden
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Liste der Bilddateien sortieren
frames = [f for f in sorted(os.listdir(frames_folder)) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Laden des ersten Frames, um die Dimensionen festzulegen
frame_path = os.path.join(frames_folder, frames[0])
frame = cv2.imread(frame_path)
height, width, layers = frame.shape

# VideoWriter initialisieren (Codec, FPS, Größe)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 30  # Frames pro Sekunde
output_path = os.path.join(output_folder, output_filename)
video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# Alle Frames hinzufügen
for frame_file in frames:
    frame_path = os.path.join(frames_folder, frame_file)
    frame = cv2.imread(frame_path)
    video.write(frame)

# Video freigeben
video.release()

print(f"Video erfolgreich gespeichert unter: {output_path}")
