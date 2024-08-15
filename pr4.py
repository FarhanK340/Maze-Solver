from collections import deque

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
    for i, direction in enumerate('NWSE'):
        if not (pos_value & (1 << (3 - i))):  # No wall in this direction
            dx, dy = directions[direction]
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]):
                if can_move(maze, (x, y), (nx, ny)):
                    neighbors.append((dx, dy, direction))
    return neighbors

def get_next_position(maze, current, dx, dy):
    x, y = current
    while True:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]):
            # Check if there is no wall in the direction of movement
            if can_move(maze, (x, y), (nx, ny)):
                x, y = nx, ny
            else:
                break
        else:
            break
    return (x, y)

def can_move(maze, current, next_pos):
    x, y = current
    nx, ny = next_pos
    current_value = maze[x][y]
    next_value = maze[nx][ny]
    direction = get_direction((x, y), (nx, ny))
    
    direction_map = {'N': 3, 'W': 2, 'S': 1, 'E': 0}
    opposite_direction_map = {'N': 1, 'W': 0, 'S': 3, 'E': 2}
    
    return (not (current_value & (1 << direction_map[direction]))) and (not (next_value & (1 << opposite_direction_map[direction])))

def get_direction(current, neighbor):
    if current[0] == neighbor[0] + 1:
        return "N"
    elif current[0] == neighbor[0] - 1:
        return "S"
    elif current[1] == neighbor[1] + 1:
        return "W"
    elif current[1] == neighbor[1] - 1:
        return "E"

# Updated BFS function to utilize the new `get_next_position` logic
def bfs(maze, source, destination):
    interval = 0
    queue = deque([(source, [""])])
    visited = {source}

    while queue:
        next_queue = deque()
        for _ in range(len(queue)):
            current, path = queue.popleft()

            if current == destination:
                return path

            for neighbor in get_neighbors(maze, current):
                next_pos = get_next_position(maze, current, neighbor[0], neighbor[1])
                if next_pos not in visited:
                    visited.add(next_pos)
                    new_path = path[:]
                    if len(new_path) <= interval:
                        new_path.append("")
                    new_path[interval] += neighbor[2]
                    next_queue.append((next_pos, new_path))

        queue = next_queue
        maze = rotate_map(maze)
        interval += 1
        visited = set()  # Reset visited for the new interval

    return None

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

    path = bfs(ar, source, destination)

    if path is None:
        return None
    return path

# Test Example
maze = [
    [6, 3, 10, 4, 11],
    [8, 10, 4, 8, 5],
    [-1, 14, 11, 3, -2],  # Start position 'B' replaced with -1 and Destination 'X' replaced with -2
    [15, 3, 4, 14, 15],
    [14, 7, 15, 5, 5]
]

print(maze_solver(maze))  # Expected Output: ['', '', 'E', '', 'E', 'NESE']
