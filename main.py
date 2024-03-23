# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com
import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data


def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


def get_possible_moves(game_state: typing.Dict):

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    # Check if moving up will be within bounds
    if my_head["y"] == board_height - 1:
        is_move_safe["up"] = False

    # Check if moving down will be within bounds
    if my_head["y"] == 0:
        is_move_safe["down"] = False

    # Check if moving left will be within bounds
    if my_head["x"] == 0:
        is_move_safe["left"] = False

    # Check if moving right will be within bounds
    if my_head["x"] == board_width - 1:
        is_move_safe["right"] = False

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']

    # Iterates through each segment of the snake body
    for body_segment in my_body[1:]:

        # Check if moving up would cause collision
        if my_head["x"] == body_segment["x"] and my_head["y"] + 1 == body_segment["y"]:
            is_move_safe["up"] = False

        # Check if moving down would cause collision
        if my_head["x"] == body_segment["x"] and my_head["y"] - 1 == body_segment["y"]:
            is_move_safe["down"] = False

        # Check if moving left would cause collision
        if my_head["x"] - 1 == body_segment["x"] and my_head["y"] == body_segment["y"]:
            is_move_safe["left"] = False

        # Check if moving right would cause collision
        if my_head["x"] + 1 == body_segment["x"] and my_head["y"] == body_segment["y"]:
            is_move_safe["right"] = False

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    # opponents = game_state['board']['snakes']
    opponents = game_state['board']['snakes']
    for snake in opponents:
        for body_segment in snake['body']:
            # collision moving up
            if my_head["x"] == body_segment["x"] and my_head["y"] + 1 == body_segment["y"]:
                is_move_safe["up"] = False
            # collision moving down
            if my_head["x"] == body_segment["x"] and my_head["y"] - 1 == body_segment["y"]:
                is_move_safe["down"] = False
            # collision moving left
            if my_head["x"] - 1 == body_segment["x"] and my_head["y"] == body_segment["y"]:
                is_move_safe["left"] = False
            # collision moving right
            if my_head["x"] + 1 == body_segment["x"] and my_head["y"] == body_segment["y"]:
                is_move_safe["right"] = False

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    return safe_moves


def is_terminal_state(game_state: typing.Dict):
    if len(get_possible_moves(game_state)) == 0:
        return True
    else:
        return False


def evaluate(game_state):
    my_snake = game_state['you']
    my_head = my_snake['body'][0]
    board = game_state['board']
    snakes = board['snakes']
    food = board['food']

    # Define weights for different factors affecting the evaluation
    snake_length_weight = 1
    food_weight = 2
    danger_weight = -5

    # Score based on snake length (longer snake is generally better)
    score = len(my_snake['body']) * snake_length_weight

    # Score based on proximity to food
    closest_food_distance = float('inf')
    for food_item in food:
        distance_to_food = abs(
            my_head['x'] - food_item['x']) + abs(my_head['y'] - food_item['y'])
        closest_food_distance = min(closest_food_distance, distance_to_food)
    # Add 1 to avoid division by zero
    score += food_weight / (closest_food_distance + 1)

    # Score based on proximity to other snakes (avoidance of danger)
    for snake in snakes:
        if snake['id'] != my_snake['id']:  # Exclude own snake
            for body_segment in snake['body']:
                distance_to_snake = abs(
                    my_head['x'] - body_segment['x']) + abs(my_head['y'] - body_segment['y'])
                if distance_to_snake == 1:  # Immediate danger
                    score += danger_weight
    return score


def simulate_move(game_state, move):
    new_state = game_state
    # Update the position of snake's head based on the move
    head = new_state['you']['body'][0]
    if move == "up":
        head['y'] += 1
    elif move == "down":
        head['y'] -= 1
    elif move == "left":
        head['x'] -= 1
    elif move == "right":
        head['x'] += 1
    # Check for collisions with food and update snake's length and health
    for food in new_state['board']['food']:
        if head['x'] == food['x'] and head['y'] == food['y']:
            # Remove the consumed food
            new_state['board']['food'].remove(food)
            # Increase snake's length and health
            new_state['you']['length'] += 1
            new_state['you']['health'] = min(
                100, new_state['you']['health']+25)  # increase health
    # Check for collisions with other snakes
    for snake in new_state['board']['snakes']:
        if snake['id'] != new_state['you']['id']:
            for segment in snake['body']:
                if head['x'] == segment['x'] and head['y'] == segment['y']:
                    new_state['you']['health'] = 0  # snake death
    if new_state['you']['length'] > 1:
        new_state['you']['body'] = [head] + new_state['you']['body'][:1]
    else:
        new_state['you']['body'] = [head]
    return new_state


def minimax(game_state, depth, maximizing_player):
    if depth == 0 or is_terminal_state(game_state):
        return evaluate(game_state), None

    if maximizing_player:
        best_value = float("-inf")
        best_move = None
        for move_option in get_possible_moves(game_state):
            new_state = simulate_move(game_state, move_option)
            value = minimax(new_state, depth - 1, False)[0]
            if value > best_value:
                best_value = value
                best_move = move_option
        return best_value, best_move
    else:
        best_value = float("inf")
        best_move = None
        for move_option in get_possible_moves(game_state):
            new_state = simulate_move(game_state, move_option)
            value = minimax(new_state, depth - 1, True)[0]
            if value < best_value:
                best_value = value
                best_move = move_option
        return best_value, best_move


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data


def move(game_state: typing.Dict) -> typing.Dict:

    next_move = minimax(game_state, 3, True)[1]

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
