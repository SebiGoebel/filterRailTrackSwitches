import json

# Datei einlesen
with open('rs19_egopath.json', 'r') as file:
    data = json.load(file)

# Initialisieren von Zählvariablen
total_left_rail_points = 0
total_right_rail_points = 0
image_count = 0

# Alle Punkte aus den Bildern zählen
for image, rails in data.items():
    total_left_rail_points += len(rails["left_rail"])
    total_right_rail_points += len(rails["right_rail"])
    left_rail_count = len(rails["left_rail"])
    right_rail_count = len(rails["right_rail"])
    print(f"{image}: Left Rail Points = {left_rail_count}, Right Rail Points = {right_rail_count}")
    image_count += 1

print("------------")

# Durchschnitt der Anzahl der Punkte berechnen
average_left_rail_points = total_left_rail_points / image_count
average_right_rail_points = total_right_rail_points / image_count

print(f"total_left_rail_points: {total_left_rail_points}")
print(f"total_right_rail_points: {total_right_rail_points}")

print("------------")

# Ergebnisse ausgeben
print(f"Average Number of Left Rail Points: {average_left_rail_points}")
print(f"Average Number of Right Rail Points: {average_right_rail_points}")

print("------------")

print(f"image_count: {image_count}")
print("image_count soll 7917 sein weil 8500 - 583 = 7917")

print("------------")