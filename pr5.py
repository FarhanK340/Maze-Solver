from collections import deque

# Function to rotate the value of a cell 90 degrees clockwise
def rotate_value(value):
    return ((value << 1) | (value >> 3)) & 0b1111

# Function to rotate the entire maze
def rotate_map(ar):
    rotated_maze = []
    for row in ar:
        rotated_row = []
        for cell in row:
            if isinstance(cell, int) and cell != -1 and cell != -2:
                rotated_row.append(rotate_value(cell))
            else:
                rotated_row.append(cell)
        rotated_maze.append(rotated_row)
    return rotated_maze

# Function to check if the move is valid
def can_move(maze, current, next_pos):
    x, y = current
    nx, ny = next_pos
    current_value = maze[x][y]
    next_value = maze[nx][ny]
    direction = get_direction((x, y), (nx, ny))
    
    direction_map = {'N': 3, 'W': 2, 'S': 1, 'E': 0}
    opposite_direction_map = {'N': 1, 'W': 0, 'S': 3, 'E': 2}
    
    return (not (current_value & (1 << direction_map[direction]))) and (not (next_value & (1 << opposite_direction_map[direction])))

# Function to get the direction from current cell to neighbor
def get_direction(current, neighbor):
    if current[0] == neighbor[0] + 1:
        return "N"
    elif current[0] == neighbor[0] - 1:
        return "S"
    elif current[1] == neighbor[1] + 1:
        return "W"
    elif current[1] == neighbor[1] - 1:
        return "E"

# Function to get neighbors of the current cell considering the maze and rotation
def get_neighbors(maze, current):
    neighbors = []
    x, y = current
    directions = {
        'N': (-1, 0),
        'W': (0, -1),
        'S': (1, 0),
        'E': (0, 1)
    }

    pos_value = maze[x][y]
    
    if pos_value == -1:
        pos_value = 0
    for i, direction in enumerate('NWSE'):
        if not (pos_value & (1 << (3 - i))):  # No wall in this direction
            dx, dy = directions[direction]
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]):
                if can_move(maze, (x, y), (nx, ny)):
                    neighbors.append((dx, dy, direction))
    return neighbors

# Function to get the next position in the given direction until a wall is hit
def get_next_position(maze, current, dx, dy):
    x, y = current
    while True:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]):
            if can_move(maze, (x, y), (nx, ny)):
                x, y = nx, ny
            else:
                break
        else:
            break
    return (x, y)

# Backtracking with dynamic programming function to find the shortest path
def backtrack(maze, current, destination, memo, path, visited):
    if current == destination:
        return path

    if current in memo:
        return memo[current]

    visited.add(current)
    shortest_path = None

    for dx, dy, direction in get_neighbors(maze, current):
        next_pos = get_next_position(maze, current, dx, dy)
        if next_pos not in visited:
            new_path = path + [direction]
            result = backtrack(maze, next_pos, destination, memo, new_path, visited)
            if result is not None:
                if shortest_path is None or len(result) < len(shortest_path):
                    shortest_path = result

    visited.remove(current)
    memo[current] = shortest_path
    return shortest_path

# Main function to solve the maze
def maze_solver(ar):
    source, destination = None, None

    # Find start and end positions
    for i in range(len(ar)):
        for j in range(len(ar[0])):
            if ar[i][j] == -1:
                source = (i, j)
            elif ar[i][j] == -2:
                destination = (i, j)

    if source is None or destination is None:
        return "No path found"

    memo = {}
    visited = set()
    path = backtrack(ar, source, destination, memo, [], visited)

    if path is None:
        return None
    return path

# Test Example
maze =  [
    [4, 2, 5, 4],
    [4, 15, 11, 1],
    [-1, 9, 6, 8],  # Start position 'B' replaced with -1
    [12, 7, 7, -2]  # Destination 'X' replaced with -2  
]

print(maze_solver(maze)) 
