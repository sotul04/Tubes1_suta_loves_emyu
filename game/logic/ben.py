import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction


class FiveLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        # print(props)
        # Analyze new state
        print(props.diamonds)
        if (props.diamonds >= 3):
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
            print("udah 3, balik ke base")
        else:
            # 
            for i in board.game_objects:
                if i.type == "DiamondGameObject":
                    self.goal_position = i.position
                    break
            print("cari lagi...")

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
            pass
            # Roam around
            # for i in board.game_objects:
            #     if i.type == "DiamondGameObject":
            #         self.goal_position = i.position
        return delta_x, delta_y
