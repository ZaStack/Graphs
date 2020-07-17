from room import Room
from player import Player
from world import World
import random
from ast import literal_eval

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
directions = {'n':'s', 's':'n', 'e':'w', 'w':'e'}
path = []
explored = {}

# Add first room at 0 index of explored and attach the available exits
explored[player.current_room.id] = player.current_room.get_exits()
# Go to each room and through each exit, remove each visited exit until none are left. When dead end is reached, go back
while len(explored) < len(room_graph) - 1:
    # if ID of current room not in explored
    if player.current_room.id not in explored:
        # add it and the exits
        explored[player.current_room.id] = player.current_room.get_exits()
        # Previous path is the direction you came from
        previous_path = path[-1]
        # Remove previous path from unexpolored exits
        explored[player.current_room.id].remove(previous_path)
    # If it is in explored but has no unexplored exits
    while len(explored[player.current_room.id]) < 1:
        # Take previous direction traveled
        previous_path = path.pop()
        # Add to final traversal_path
        traversal_path.append(previous_path)
        # Return to last room and check for exits
        player.travel(previous_path)
    # If room is in explored and has unexplored exits, set next path to the first direction in exit list
    next_path = explored[player.current_room.id].pop(0)
    #  Add next path to the final traversal_path
    traversal_path.append(next_path)
    # Add the opposite of next path to the end of path as the direction you just came from
    path.append(directions[next_path])
    # Move to next room
    player.travel(next_path)




# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited"
    )
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
