from type_defs import Direction, Block_Position, add_positions
from  map import Map

class Step:
    starting: Block_Position
    direction: Direction

    def __init__(self, starting_pos: Block_Position, direction: Direction) -> None:
        self.starting = starting_pos
        self.direction = direction

class Avatar:
    pos: Block_Position
    facing: Direction

    step_memory: list[Step]

    def __init__(self, pos: Block_Position) -> None:
        self.pos = pos
        self.facing = Direction.random_direction()
        self.step_memory = []
    
    def stumble_around(self, map: Map) -> None:
        self.facing = self.facing.right()

        while not map.get(add_positions(self.pos, self.facing.deltas)).walkable:
            # print(f"{self.facing}; {self.facing.deltas}; {self.pos}; {map.get(add_positions(self.pos, self.facing.deltas))}")
            self.facing = self.facing.rotate_clockwise(-1)

        self.step_memory.append(Step(self.pos, self.facing))
        self.pos = add_positions(self.pos, self.facing.deltas)


    