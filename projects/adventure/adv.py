from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
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
visited = {}
current_room = world.starting_room
prev_dir = None
reverse_dir = {'n': 's', 'e': 'w', 'w': 'e', 's': 'n'}
while len(visited) < len(room_graph):
    exits = current_room.get_exits()
    if current_room.id not in visited:
        new_entry = {}
        for ex in exits:
            new_entry[ex] = '?'
        visited[current_room.id] = new_entry
    if prev_dir and visited[current_room.id][reverse_dir[prev_dir[1]]] == '?':
        visited[current_room.id][reverse_dir[prev_dir[1]]] = prev_dir[0]
    unexplored_exits = [
        ex for ex in exits if visited[current_room.id][ex] == '?']
    if unexplored_exits:
        travel = random.choice(unexplored_exits)
        new_room = current_room.get_room_in_direction(travel)
        visited[current_room.id][travel] = new_room.id
        prev_dir = (current_room.id, travel)
        current_room = new_room
        traversal_path.append(travel)


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
