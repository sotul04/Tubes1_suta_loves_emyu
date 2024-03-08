import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction


class ScifoLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        # Analyze new state
        if props.diamonds == 5 or (board_bot.properties.milliseconds_left < 8000 and props.diamonds > 0):
            # Move to base
            print("GO")
            base = board_bot.properties.base
            self.goal_position = base
        else:
            # Just roam around
            self.goal_position = None

        current_position = board_bot.position
        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        else:
            # Roam around
            direction_string, direction_value = self.check_direction_2(board_bot,board)
            if (direction_string == "NORTH"):
                if ((board_bot.position.y != 0 and direction_value != 0) or board_bot.position.y == board.height-1):
                    delta_x, delta_y = 0,-1
                else:
                    delta_x, delta_y = 0,1
            elif (direction_string == "WEST"):
                if ((board_bot.position.x != 0 and direction_value != 0) or board_bot.position.x == board.width-1):
                    delta_x, delta_y = -1,0
                else:
                    delta_x, delta_y = 1,0
            elif (direction_string == "EAST"):
                if ((board_bot.position.x != board.width-1 and direction_value != 0) or board_bot.position.x == 0):
                    delta_x, delta_y = 1,0
                else:
                    delta_x, delta_y = -1,0
            elif (direction_string == "SOUTH"):
                if ((board_bot.position.y != board.height-1 and direction_value != 0) or board_bot.position.y == 0):
                    delta_x, delta_y = 0,1
                else:
                    delta_x, delta_y = 0,-1
        return delta_x, delta_y
        
    def check_direction_2(self, board_bot: GameObject, board: Board):
        priority_north,priority_east,priority_west,priority_south = 0,0,0,0
        north_distance = 999
        south_distance = 999
        west_distance = 999
        east_distance = 999
        for i in range (len(board.game_objects)):
            if (board.game_objects[i].type == "DiamondGameObject"):
                if (board_bot.position.x == board.game_objects[i].position.x):
                    if (board_bot.position.y > board.game_objects[i].position.y):
                        if (board_bot.position.y - board.game_objects[i].position.y < north_distance):
                            north_distance = board_bot.position.y - board.game_objects[i].position.y
                        if (board.game_objects[i].properties.points == 1):
                            priority_north += 1
                        elif (board.game_objects[i].properties.points == 2 and board_bot.properties.diamonds < 4):
                            priority_north += 2
                    else:
                        if (board.game_objects[i].position.y - board_bot.position.y < south_distance):
                            south_distance = - board.game_objects[i].position.y - board_bot.position.y
                        if (board.game_objects[i].properties.points == 1):
                            priority_south += 1
                        elif (board.game_objects[i].properties.points == 2 and board_bot.properties.diamonds < 4):
                            priority_south += 2
                elif (board_bot.position.y == board.game_objects[i].position.y):
                    if (board_bot.position.x > board.game_objects[i].position.x):
                        if (board_bot.position.x - board.game_objects[i].position.x < west_distance):
                            west_distance = board_bot.position.x - board.game_objects[i].position.x
                        if (board.game_objects[i].properties.points == 1 and board_bot.properties.diamonds < 4):
                            priority_west += 1
                        elif (board.game_objects[i].properties.points == 2 and board_bot.properties.diamonds < 4):
                            priority_west += 2
                    else:
                        if (board.game_objects[i].position.x - board_bot.position.x < east_distance):
                            east_distance = board.game_objects[i].position.x - board_bot.position.x
                        if (board.game_objects[i].properties.points == 1 and board_bot.properties.diamonds < 4):
                            priority_east += 1
                        elif (board.game_objects[i].properties.points == 2 and board_bot.properties.diamonds < 4):
                            priority_east += 2
        print(north_distance,east_distance,west_distance,south_distance)
        print(priority_north,priority_east,priority_west,priority_south)
        print(board_bot.properties.milliseconds_left)
        return_string = ""
        return_value = max(priority_north,priority_east,priority_west,priority_south)
        if (return_value == priority_north and board_bot.position.y != 0):
            return_string = "NORTH"
            if (return_value == priority_east):
                if (north_distance > east_distance):
                    return_string = "EAST"
                else:
                    return_string = "NORTH"
            if (return_value == priority_west):
                if (north_distance > west_distance):
                    return_string = "WEST"
                else:
                    return_string = "NORTH"
            if (return_value == priority_south):
                if (north_distance > south_distance):
                    return_string = "SOUTH"
                else:
                    return_string = "NORTH"
        elif (return_value == priority_west and board_bot.position.x != 0):
            return_string = "WEST"
            if (return_value == priority_south):
                if (west_distance > south_distance):
                    return_string = "SOUTH"
                else:
                    return_string = "WEST"
            if (return_value == priority_north):
                if (west_distance > north_distance):
                    return_string = "NORTH"
                else:
                    return_string = "WEST"
            if (return_value == priority_north):
                if (west_distance > east_distance):
                    return_string = "EAST"
                else:
                    return_string = "WEST"
        elif (return_value == priority_east and board_bot.position.x != board.width-1):
            return_string = "EAST"
            if (return_value == priority_south):
                if (east_distance > south_distance):
                    return_string = "SOUTH"
                else:
                    return_string = "EAST"
            if (return_value == priority_west):
                if (east_distance > west_distance):
                    return_string = "WEST"
                else:
                    return_string = "EAST"
            if (return_value == priority_north):
                if (east_distance > north_distance):
                    return_string = "NORTH"
                else:
                    return_string = "EAST"
        elif (return_value == priority_south and board_bot.position.y != board.height-1):
            return_string = "SOUTH"
            if (return_value == priority_north):
                if (east_distance > north_distance):
                    return_string = "NORTH"
                else:
                    return_string = "SOUTH"
            if (return_value == priority_west):
                if (east_distance > west_distance):
                    return_string = "WEST"
                else:
                    return_string = "SOUTH"
            if (return_value == priority_east):
                if (east_distance > east_distance):
                    return_string = "EAST"
                else:
                    return_string = "SOUTH"
        print(return_string,return_value)
        return return_string, return_value