from room import Room
from player import Player
from world import World

import random
import math
import shelve
from ast import literal_eval
from collections import deque

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


def init_db(rooms, db):
    size = len(rooms)
    paths = {}
    for start in range(size):
        print(f"{size - start}...")
        start_room = rooms[start]
        for dest in range(size):
            dest_room = rooms[dest]
            room_paths = {start_room.id: [start_room.id]}
            q = deque()
            q.append(start_room)
            while len(q):
                head = q.popleft()
                for ex in head.get_exits():
                    new_room = head.get_room_in_direction(ex)
                    if new_room.id not in room_paths:
                        room_paths[new_room.id] = room_paths[head.id] + \
                            [new_room.id]
                        q.append(new_room)
            paths[start] = room_paths
    db['paths'] = paths


db_paths = {}

with shelve.open('db') as db:
    if 'paths' not in db or len(db['paths']) < len(world.rooms):
        print("Initializing database...")
        init_db(world.rooms, db)
    db_paths = db['paths']


def get_nearest_neighbor(current_room_id, paths, visited, greed=1):
    candidates = []
    for room_id in [_ for _ in paths if _ != current_room_id]:
        if room_id not in visited:
            candidates.append((room_id, len(paths[room_id])))
    candidates.sort(key=(lambda x: x[1]))
    nearest_neighbor = random.choice(candidates[:greed])[0]
    return nearest_neighbor


def add_directions_from_path(rooms, path, traversal):
    for i in range(len(path) - 1):
        current_room = rooms[path[i]]
        next_room_id = path[i + 1]
        for ex in current_room.get_exits():
            room = current_room.get_room_in_direction(ex)
            if room and room.id == next_room_id:
                traversal.append(ex)


trials = 10000
greed = 2
shortest_path = None

for _ in range(trials):
    current_room_id = world.starting_room.id
    current_path = [current_room_id]
    visited = {current_room_id}

    while len(visited) < len(room_graph):
        nearest_neighbor_id = get_nearest_neighbor(
            current_room_id, db_paths[current_room_id], visited, greed)
        current_path.append(nearest_neighbor_id)
        visited.add(nearest_neighbor_id)
        current_room_id = nearest_neighbor_id

    # Expand path to full list of room ids to visit
    expanded_path = [0]
    for i in range(len(current_path) - 1):
        current_room = current_path[i]
        next_room = current_path[i + 1]
        expanded_path += db_paths[current_room][next_room][1:]

    if (not shortest_path
            or len(expanded_path) < len(shortest_path)):
        shortest_path = expanded_path


# Turn path into list of directions
add_directions_from_path(world.rooms, shortest_path, traversal_path)
print(traversal_path)

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
