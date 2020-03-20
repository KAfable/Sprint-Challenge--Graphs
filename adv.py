from room import Room
from player import Player
from world import World
from util import Stack, Queue

import random
from ast import literal_eval

world = World()

map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)
world.print_rooms()
player = Player(world.starting_room)

traversal_path = []


def generate_room_path(p1):
    ''' Generates a path (list) of rooms in DFT order to explore every room.'''
    stack = Stack()
    stack.push(p1.current_room)
    visited = []

    while stack.size() > 0:
        current = stack.pop()
        if current.id not in visited:
            visited.append(current.id)
            directions = current.get_exits()
            for d in directions:
                room = current.get_room_in_direction(d)
                stack.push(room)
    return visited


def get_shortest_path(origin_id, destination_id):
    ''' Return a list of ID's containing the shortest path from starting room id, to the destination id '''
    q = Queue()
    q.enqueue([origin_id])
    visited = set()

    while q.size() > 0:
        path = q.dequeue()
        room = path[-1]
        if room not in visited:
            visited.add(room)
            if room == destination_id:
                return path
            else:
                room_exits = world.rooms[room].get_exits()
                for d in room_exits:
                    neighbor = world.rooms[room].get_room_in_direction(d)
                    q.enqueue([*path, neighbor.id])


def convert_path_to_directions(path, p1):
    ''' Given a path of rooms and a player, converts it to a list of directions for the player to follow. '''
    direction_path = []
    if p1.current_room.id != path[0]:
        print('PLayer must start in the first room of the traversal list.')
        return
    for i in range(len(path) - 1):
        direction = p1.current_room.is_neighbor(path[i+1])
        if direction:
            p1.travel(direction)
            direction_path.append(direction)
        else:
            backtrack = get_shortest_path(p1.current_room.id, path[i+1])
            for room_id in backtrack[1:]:
                direction = p1.current_room.is_neighbor(room_id)
                p1.travel(direction)
                direction_path.append(direction)
    return direction_path


    # Driver Code
room_order = generate_room_path(player)
traversal_path = convert_path_to_directions(room_order, player)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
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
