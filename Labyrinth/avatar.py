from type_defs import Direction, Block_Position, add_positions
from  map import Map

class Avatar:
    pos: Block_Position
    facing: Direction

    memory: list[Block_Position]

    def __init__(self, pos: Block_Position) -> None:
        self.pos = pos
        self.facing = Direction.random_direction()
    
    def stumble_around(self, map: Map) -> None:
        self.facing = self.facing.right()

        while not map.get(add_positions(self.pos, self.facing.deltas)).walkable:
            # print(f"{self.facing}; {self.facing.deltas}; {self.pos}; {map.get(add_positions(self.pos, self.facing.deltas))}")
            self.facing = self.facing.rotate_clockwise(-1)

        self.pos = add_positions(self.pos, self.facing.deltas)