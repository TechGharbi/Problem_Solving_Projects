from model import Car, Node

def load_map_level(level: int) -> Node:
    path = f"Map/{level}.txt"
    with open(path, 'r') as f:
        raw = [line.strip() for line in f.readlines() if line.strip()]

    if len(raw) != 10 or any(len(row) != 10 for row in raw):
        raise ValueError("❌ La carte doit avoir une taille de 10x10.")

    cars = {}
    for row in range(2, 8):
        for col in range(2, 8):
            ch = raw[row][col]
            if ch not in ['-', 'X'] and ch not in cars:
                # Tìm chiều dài và hướng
                dir = 'h'
                size = 1
                if col + 1 < 10 and raw[row][col + 1] == ch:
                    dir = 'h'
                    while col + size < 10 and raw[row][col + size] == ch:
                        size += 1
                elif row + 1 < 10 and raw[row + 1][col] == ch:
                    dir = 'v'
                    while row + size < 10 and raw[row + size][col] == ch:
                        size += 1
                cars[ch] = Car(id=ch, dir=dir, row=row, col=col, size=size)

    return Node(list(cars.values()))
