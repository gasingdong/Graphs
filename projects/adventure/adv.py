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
    size = len(world.rooms)
    paths = {}
    for start in range(size):
        print(f"{size - start}...")
        start_room = world.rooms[start]
        for dest in range(size):
            dest_room = world.rooms[dest]
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

trials = 100
shortest_traversal = None
for _ in range(trials):
    temp_traversal = []
    current_room = world.starting_room.id
    tsp = [current_room]
    visited = {current_room}

    while len(visited) < len(room_graph):
        nearest_neighbor = None
        current_shortest = None
        current_dict = db_paths[current_room]
        for room_id in current_dict:
            if room_id not in visited:
                if (room_id != current_room and
                    (not current_shortest or
                     (len(current_dict[room_id]) <= current_shortest))):
                    if len(current_dict[room_id]) == current_shortest:
                        if random.randint(0, 1) == 1:
                            current_shortest = len(current_dict[room_id])
                            nearest_neighbor = room_id
                    else:
                        current_shortest = len(current_dict[room_id])
                        nearest_neighbor = room_id
        tsp.append(nearest_neighbor)
        visited.add(nearest_neighbor)
        current_room = nearest_neighbor

    full_path = [0]

    for i in range(len(tsp) - 1):
        current_room = tsp[i]
        next_room = tsp[i + 1]
        shortest_path = db_paths[current_room][next_room][1:]
        full_path = full_path + shortest_path

    for i in range(len(full_path) - 1):
        current_room = world.rooms[full_path[i]]
        next_room_id = full_path[i + 1]
        for ex in current_room.get_exits():
            room = current_room.get_room_in_direction(ex)
            if room and room.id == next_room_id:
                temp_traversal.append(ex)
    if not shortest_traversal or len(temp_traversal) < len(shortest_traversal):
        shortest_traversal = temp_traversal

traversal_path = shortest_traversal
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
