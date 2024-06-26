# Beispiel-Polygonpunkte
polygon_points = [(2, 3), (5, 11), (12, 8), (9, 5), (5, 6)]

# Eine Funktion, um die min und max x-Werte für jede y-Koordinate zu finden
def find_edges(polygon_points):
    # Dictionary, um min und max x-Werte für jede y-Koordinate zu speichern
    edges = {}
    
    for x, y in polygon_points:
        if y in edges:
            edges[y]['min'] = min(edges[y]['min'], x)
            edges[y]['max'] = max(edges[y]['max'], x)
        else:
            edges[y] = {'min': x, 'max': x}
    
    return edges

# Kanten des Polygons finden
edges = find_edges(polygon_points)

# Ergebnisse anzeigen
for y in sorted(edges):
    print(f"y = {y}: min x = {edges[y]['min']}, max x = {edges[y]['max']}")
