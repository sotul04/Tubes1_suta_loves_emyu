import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction


class NearestLogic(BaseLogic):
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
            delta_x,delta_y = self.get_least_steps(board_bot,board)
        return delta_x, delta_y
    
    def get_least_steps(self, board_bot: GameObject, board: Board):
        min_steps_num = 999999
        min_steps_x,min_steps_y = 0,0
        for i in range(len(board.game_objects)):
            if (board.game_objects[i].type == "DiamondGameObject" or board.game_objects[i].type == "DiamondButtonGameObject"):
                steps = abs(abs(board_bot.position.x-board.game_objects[i].position.x)+abs(board_bot.position.y-board.game_objects[i].position.y))
                if (steps < min_steps_num and steps != 0):
                    if (not (board.game_objects[i].properties.points == 2 and board_bot.properties.diamonds == 4)):
                        min_steps_num = steps
                        min_steps_x,min_steps_y = board.game_objects[i].position.x,board.game_objects[i].position.y
                elif (steps == min_steps_num and steps != 0):
                    target_to_home = abs(board.game_objects[i].position.x-board_bot.properties.base.x)+abs(board.game_objects[i].position.y-board_bot.properties.base.y)
                    current_to_home = abs(min_steps_x-board_bot.properties.base.x)+abs(min_steps_y-board_bot.properties.base.y)
                    if (target_to_home < current_to_home):
                        if (not (board.game_objects[i].properties.points == 2 and board_bot.properties.diamonds == 4)):
                            min_steps_num = steps
                            min_steps_x,min_steps_y = board.game_objects[i].position.x,board.game_objects[i].position.y
        home = abs(abs(board_bot.position.x-board_bot.properties.base.x)+abs(board_bot.position.y-board_bot.properties.base.y))
        if (home <= 2 and board_bot.properties.diamonds >= 3):
            delta_x,delta_y = get_direction(board_bot.position.x,board_bot.position.y,board_bot.properties.base.x,board_bot.properties.base.y)
        else:
            delta_x,delta_y = get_direction(board_bot.position.x,board_bot.position.y,min_steps_x,min_steps_y)
        if (delta_x == 0 and delta_y == 0):
            north = board_bot.position.y
            south = board.height-board_bot.position.y
            west = board_bot.position.x
            east = board.width-board_bot.position.x
            nearest = max(north,south,west,east)
            if (nearest == north):
                delta_x,delta_y = 0,-1
            elif (nearest == south):
                delta_x,delta_y = 0,1
            elif (nearest == west):
                delta_x,delta_y = -1,0
            elif (nearest == east):
                delta_x,delta_y = 1,0
        return delta_x,delta_y