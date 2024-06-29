def load_coordinates(file_path='coordinates.txt'):
    coordinates = {}
    with open(file_path, 'r') as f:
        for line in f:
            key, value = line.strip().split(': ')
            x, y = map(int, value.split(', '))
            coordinates[key] = (x, y)
    return coordinates
