from collections import deque
import heapq


graph = {
    'A': [('B',1), ('C',2)],
    'B': [('D',4), ('E',2)],
    'C': [('F',3)],
    'D': [],
    'E': [('G',1)],
    'F': [('G',5)],
    'G': []
}


def bfs(start, goal):
    visited = set()
    queue = deque([(start, [])])

    while queue:
        node, path = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        path = path + [node]
        if node == goal:
            return path
        for neighbor, _ in graph[node]:
            queue.append((neighbor, path))
    return None


def dfs(start, goal):
    visited = set()
    stack = [(start, [])]

    while stack:
        node, path = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        path = path + [node]
        if node == goal:
            return path
        for neighbor, _ in graph[node]:
            stack.append((neighbor, path))
    return None


def uniform_cost_search(start, goal):
    visited = set()
    heap = [(0, start, [])]

    while heap:
        cost, node, path = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        path = path + [node]
        if node == goal:
            return path, cost
        for neighbor, edge_cost in graph[node]:
            heapq.heappush(heap, (cost + edge_cost, neighbor, path))
    return None


def depth_limited_search(start, goal, limit):
    def recursive(node, path, depth):
        if node == goal:
            return path + [node]
        if depth == limit:
            return None
        for neighbor, _ in graph[node]:
            result = recursive(neighbor, path + [node], depth + 1)
            if result:
                return result
        return None
    return recursive(start, [], 0)


def iterative_deepening_dfs(start, goal, max_depth):
    for depth in range(max_depth + 1):
        result = depth_limited_search(start, goal, depth)
        if result:
            return result
    return None


def construct_path(meeting, visited_start, visited_goal):
    path_start = []
    node = meeting
    while node is not None:
        path_start.append(node)
        node = visited_start[node]
    path_start.reverse()

    path_goal = []
    node = visited_goal[meeting]
    while node is not None:
        path_goal.append(node)
        node = visited_goal[node]

    return path_start + path_goal


def bidirectional_search(start, goal):
    if start == goal:
        return [start]

    visited_start = {start: None}
    visited_goal = {goal: None}

    queue_start = deque([start])
    queue_goal = deque([goal])

    while queue_start and queue_goal:

        node = queue_start.popleft()
        for neighbor, _ in graph[node]:
            if neighbor not in visited_start:
                visited_start[neighbor] = node
                queue_start.append(neighbor)
            if neighbor in visited_goal:
                return construct_path(neighbor, visited_start, visited_goal)

        node = queue_goal.popleft()
        for neighbor, _ in graph[node]:
            if neighbor not in visited_goal:
                visited_goal[neighbor] = node
                queue_goal.append(neighbor)
            if neighbor in visited_start:
                return construct_path(neighbor, visited_start, visited_goal)

    return None


start = 'A'
goal = 'G'

print("BFS:", bfs(start, goal))
print("DFS:", dfs(start, goal))
print("UCS:", uniform_cost_search(start, goal))
print("DLS (limit=3):", depth_limited_search(start, goal, 3))
print("IDDFS:", iterative_deepening_dfs(start, goal, 5))
print("Bidirectional:", bidirectional_search(start, goal))
