from room import Room
from player import Player
from world import World

import random
import math
from ast import literal_eval
from collections import deque

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

dist_mat = [[0] * len(world.rooms) for _ in range(len(world.rooms))]
all_paths = {}

for start in range(len(world.rooms)):
    print("start", start)
    start_room = world.rooms[start]
    for dest in range(len(world.rooms)):
        dest_room = world.rooms[dest]
        paths = {start_room.id: [start_room.id]}
        q = deque()
        q.append(start_room)
        while len(q):
            head = q.popleft()
            for ex in head.get_exits():
                new_room = head.get_room_in_direction(ex)
                if new_room.id not in paths:
                    paths[new_room.id] = paths[head.id] + [new_room.id]
                    q.append(new_room)
        dist = len(paths[dest]) - 1
        dist_mat[start][dest] = dist
        dist_mat[dest][start] = dist
        all_paths[start] = paths

current_room = world.starting_room.id
tsp = [current_room]
visited = {current_room}

while len(visited) < len(room_graph):
    nearest_neighbor = None
    current_shortest = None
    current_dict = all_paths[current_room]
    for room_id in current_dict:
        if room_id not in visited:
            if (room_id != current_room and
                (not current_shortest or
                 (len(current_dict[room_id]) < current_shortest))):
                current_shortest = len(current_dict[room_id])
                nearest_neighbor = room_id
    tsp.append(nearest_neighbor)
    visited.add(nearest_neighbor)
    current_room = nearest_neighbor

print(tsp)
full_path = [0]

for i in range(len(tsp) - 1):
    current_room = tsp[i]
    next_room = tsp[i + 1]
    shortest_path = all_paths[current_room][next_room][1:]
    full_path = full_path + shortest_path

for i in range(len(full_path) - 1):
    current_room = world.rooms[full_path[i]]
    next_room_id = full_path[i + 1]
    for ex in current_room.get_exits():
        room = current_room.get_room_in_direction(ex)
        if room and room.id == next_room_id:
            traversal_path.append(ex)

print(full_path)
print(traversal_path)


# visited = {}
# current_room = world.starting_room
# prev_dir = None
# reverse_dir = {'n': 's', 'e': 'w', 'w': 'e', 's': 'n'}

# while len(visited) < len(room_graph):
#     exits = current_room.get_exits()
#     if current_room.id not in visited:
#         new_entry = {}
#         for ex in exits:
#             new_entry[ex] = '?'
#         visited[current_room.id] = new_entry
#     if (prev_dir
#       and visited[current_room.id][reverse_dir[prev_dir[1]]] == '?'):
#         visited[current_room.id][reverse_dir[prev_dir[1]]] = prev_dir[0]
#     unexplored_exits = [
#         ex for ex in exits if visited[current_room.id][ex] == '?']
#     if unexplored_exits:
#         travel = random.choice(unexplored_exits)
#         new_room = current_room.get_room_in_direction(travel)
#         visited[current_room.id][travel] = new_room.id
#         prev_dir = (current_room.id, travel)
#         player.travel(travel)
#         current_room = new_room
#         traversal_path.append(travel)
#     else:
#         paths = {current_room.id: ([current_room.id], [])}
#         q = deque()
#         q.append(current_room)
#         shortest = None
#         while len(q) and not shortest:
#             head = q.popleft()
#             for ex in head.get_exits():
#                 if visited[head.id][ex] == '?':
#                     shortest = paths[head.id]
#                     break
#                 room = head.get_room_in_direction(ex)
#                 if room.id not in paths:
#                     paths[room.id] = (paths[head.id][0] +
#                                       [room.id], paths[head.id][1] + [ex])
#                     q.append(room)
#         if shortest:
#             for d in shortest[1]:
#                 travel = d
#                 player.travel(travel)
#                 traversal_path.append(travel)
#                 prev_dir = (current_room.id, travel)
#                 current_room = player.current_room
#         elif len(visited) < len(room_graph):
#             print("WARNING: No solution possible, ending search")
#             break


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves",
        f"{len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
