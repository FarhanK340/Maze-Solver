from collections import deque

def maze_solver(ar):
    
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
    
    def get_neighbors(maze, current):
        neighbors = []
        possible_moves = {
            0: [(0,1), (0,-1), (1,0), (-1,0)],
            1: [(0,-1), (1,0), (-1,0)],
            2: [(0,1), (0,-1), (-1,0)],
            3: [(0,-1), (-1,0)],
            4: [(0,1), (1,0), (-1,0)],
            5: [(1,0), (-1,0)],
            6: [(0,1), (-1,0)],
            7: [(-1,0)],
            8: [(0,1), (0,-1), (1,0)],
            9: [(0,-1), (1,0)],
            10: [(0,1), (0,-1)],
            11: [(0,-1)],
            12: [(0,1), (1,0)],
            13: [(1,0)],
            14: [(0,1)],
            15: []
        }
        
        pos = maze[current[0]][current[1]]
        if pos == -1:
            pos = 0
        if pos in possible_moves:
            for dx, dy in possible_moves[pos]:
                x, y = current[0] + dx, current[1] + dy
                if 0 <= x < len(maze) and 0 <= y < len(maze[0]):
                    neighbors.append((x, y))  
        
        # Filter out neighbors that do not consider the current position as their neighbor
        filtered_neighbors = []
        for neighbor in neighbors:
            n_row, n_col = neighbor
            n_value = maze[n_row][n_col]
            
            if n_value == -2:
                n_value = 0
            
            if n_value in possible_moves:
                is_neighbor = False
                for dx, dy in possible_moves[n_value]:
                    if (n_row + dx, n_col + dy) == current:
                        is_neighbor = True
                        break
                if is_neighbor:
                    filtered_neighbors.append(neighbor)
        
        return filtered_neighbors


    def bfs(maze, source):
        visited = set()
        queue = [(source, '')]
        paths = []
        interval = 0
        
        while True:
            if interval == 4:
                break
            while queue:
                (current, path) = queue.pop(0)
                # if(current in visited):
                #     continue
                visited.add(current)
                
                if maze[current[0]][current[1]] == -2:
                    paths.append(path)
                    return paths  # Found the destination, no need to continue BFS
                
                for neighbor in get_neighbors(maze, current):
                    if neighbor not in visited:
                        queue.append((neighbor, path + get_direction(current, neighbor)))
                        # paths[neighbor] = path + get_direction(current, neighbor)
            paths.append(path)
            queue = [(current, '')]
            interval += 1
            maze = rotate_map(maze)
                            
        return paths
    
    def get_direction(current, neighbor):
        if current[0] == neighbor[0] + 1:
            return "N"
        elif current[0] == neighbor[0] - 1:
            return "S"
        elif current[1] == neighbor[1] + 1:
            return "W"
        elif current[1] == neighbor[1] - 1:
            return "E"
        
        
    # Convert the tuple to the desired list with replacements
    ar = [[-1 if cell == 'B' else -2 if cell == 'X' else cell for cell in row] for row in ar]

    source, destination = None, None    
    
    for i in range(len(ar)):
        for j in range(len(ar[0])):
            if ar[i][j] == -1:
                source = (i, j)
            if ar[i][j] == -2:
                destination = (i, j)

    if source is None or destination is None:
        return "No path found"

#     pc = bfs(ar, source)
 
    return bfs(ar,source)
    

maze = (
    (6,3,10,4,11),
    (8,10,4,8,5),
    ('B',14,11,3,'X'),
    (15,3,4,14,15),
    (14,7,15,5,5)
)

# maze_solver(maze)
print(maze_solver(maze))   # ['', '', 'E', '', 'E', 'NESE']