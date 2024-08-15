def maze_solver(maze):
    print('\n'.join(map(str,maze)))
    
    queue = []

    def start_end_position(maze):
        start, end = None, None
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                if maze[i][j] == -1:
                    start = (i, j)
                if maze[i][j] == -2:
                    end = (i, j)
                if start is not None and end is not None:
                    return start, end
                
    def format_maze(maze):
        return [[-1 if cell == 'B' else -2 if cell == 'X' else cell for cell in row] for row in maze]

    def move(position, direction):
        if direction == 'N':
            return (position[0] - 1, position[1])
        elif direction == 'W':
            return (position[0], position[1] - 1)
        elif direction == 'S':
            return (position[0] + 1, position[1])
        elif direction == 'E':
            return (position[0], position[1] + 1)
        else:
            raise ValueError("Invalid direction")

    def valid(next_position, current_position, direction, maze):
        
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
        
        directions = {
            'N': (-1,0),
            'W': (0,-1),
            'S': (1,0),
            'E': (0,1),
        }
        
        current_val = maze[current_position[0]][current_position[1]]
        if current_val == -1:
            current_val = 0
            
        new_val = maze[next_position[0]][next_position[1]] 
        if new_val == -1 or new_val == -2:
            new_val = 0

        if direction in directions:
            move = directions[direction]
            if move in possible_moves[current_val]:
                opposite = tuple(-x for x in move)
                if opposite in possible_moves[new_val]:
                    return True
        return False

    def rotate_value(value):
        return ((value << 1) | (value >> 3)) & 0b1111

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
    
    maze = format_maze(maze)
    
    start, end = start_end_position(maze)
    
    shortest_path = []
    intervals = 0

    def dfs(current_position, current_path, intervals, maze , visited):
        nonlocal shortest_path
        if current_position not in visited:
            visited.append(current_position)
        
        shortest_path.append((current_path, current_position, visited))
        
        if current_position == end:
            return current_path
        
        for direction in ['N', 'W', 'S', 'E']:
            
            next_position = move(current_position, direction)
            if next_position[0] < 0 or next_position[0] >= len(maze) or next_position[1] < 0 or next_position[1] >= len(maze[0]):
                continue
            if  next_position not in visited and valid(next_position,current_position, direction, maze):
                result = dfs(next_position, current_path + direction, intervals, maze, visited.copy())
                if result:
                    return result
                        
        return None
    
    timestamp = 0
    record = []
    
    if intervals == 0:
        path = dfs(start, "", intervals, maze, [])
        
        if path:
            print([path])
            return [path]
        for path, position, visited in shortest_path:
            new_path = "".join(path)
            record.append(new_path)
            queue.append((path, position, timestamp, record, visited))
            record = []
            
        timestamp += 1
        shortest_path = []
        intervals += 1
        maze = rotate_map(maze)
    
    while intervals < 10:
        
        current_timstamp = None
        while queue:
            current_item = queue[0]
            if current_timstamp is not None and current_timstamp != current_item[2]:
                break
            
            current_item = queue.pop(0)
            current_path = current_item[0]
            current_position = current_item[1]
            current_timstamp = current_item[2]
            current_record = current_item[3]
            current_visited = current_item[4]
            if current_position == end:
                return current_path
            path = dfs(current_position, current_path, intervals, maze, current_visited)
            
            if path:
                for pos in shortest_path:
                    position = pos[1]
                    if position == end:
                        temp_record = current_record.copy()
                        new_path = path[len(current_path):]
                        temp_record.append(new_path)
                        print(temp_record)
                        return temp_record
                         

            for path, position, visited in shortest_path:
                temp_record = current_record.copy()
                if path == '' or current_path == path:
                    temp_record.append('')
                else:
                    new_path = path[len(current_path):]
                    temp_record.append(new_path)
                    new_path = ""
                queue.append((path, position, timestamp, temp_record, visited))
                    
            shortest_path = []
            
        timestamp += 1
        intervals += 1
        maze = rotate_map(maze)
        
    return None