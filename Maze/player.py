from map import Map
from time import sleep

class Player:
    def __init__(self,map: Map):
        self.current_map = map
        self.current_position = tuple(self.current_map.get_start())
        self.visited_pos= set()
        self.view = 0                                                              #start looking down

    def position(self):  
        return self.current_position

    def move(self):
        self.visited_pos.add(self.current_position)

        self.view = (self.view + 90) % 360                                         #look right
        spot= find_spot(self.view, self.current_position)
        if self.current_map.check_coordinate(spot) == "Path":
            self.current_position = spot
            return 
        
        while self.current_map.check_coordinate(spot) != "Path":                   #look straight,left,back
            self.view = (self.view - 90) % 360  
            spot= find_spot(self.view, self.current_position)
        self.current_position=spot
           

    def seen_pos(self):
        return self.visited_pos
    



def find_spot(view, position):
    x= position[0]
    y= position[1]
    if view == 0: spot = (x , y+1)
    if view == 90: spot= (x-1 , y)
    if view == 180: spot= (x , y-1) 
    if view == 270: spot = (x+1, y)
    return spot

def test():
    map_test= Map(r"Maze/mazes/Labyrinth-2.txt")
    player_test = Player(map_test)
    print(player_test.position())
    print(map_test.get_finish())
    while player_test.position() != map_test.get_finish():
        player_test.move()
        print(player_test.position())
        sleep(0.05)
    print(player_test.seen_pos())
    print(player_test.current_position)


if __name__ == '__main__':
    test()