def load_coordinates(file_path='coordinates.txt'):
    coordinates = {}
    colors = {}
    with open(file_path, 'r') as f:
        for line in f:
            if '_color' in line:
                key, value = line.strip().split(': ')
                colors[key.replace('_color', '')] = tuple(map(int, value.split(', ')))
            else:
                key, value = line.strip().split(': ')
                coordinates[key] = tuple(map(int, value.split(', ')))
    return coordinates, colors
