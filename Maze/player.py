from map import Map
from time import sleep

class Player:

    def __init__(self,map: Map):
        self.current_map = map
        self.current_position = tuple(map.get_start())
        self.visited_pos= set()
        self.view = 0                          #start looking down
        return None

    def position(self):  
        return self.current_position

    def move(self):
        self.visited_pos.add(self.current_position)

        self.view = (self.view + 90) % 360                                              #look right
        spot= find_spot(self.view, self.current_position)
        if self.current_map.check_coordinate(spot[0],spot[1]) == "Path":
            self.current_position = spot
            return None
        
        while self.current_map.check_coordinate(spot[0],spot[1]) != "Path":
            self.view = (self.view - 90) % 360  
            spot= find_spot(self.view, self.current_position)
        self.current_position=spot
           

    def seen_pos(self):
        return self.visited_pos
    



def find_spot(view, position):
    x= position[0]
    y= position[1]
    if view == 90:
        spot=(x - 1 , y)

    if view == 0:
        spot = (x , y + 1)

    if view == 270:
        spot = (x + 1, y)

    if view == 180:
        spot= (x , y - 1) 
    
    return spot

def test():
    map_test= Map(r"Maze/mazes/Labyrinth-2.txt")
    player = Player(map_test)
    print(player.position())
    print(map_test.get_finish())
    while player.position() != map_test.get_finish():
        player.move()
        print(player.position())
        sleep(0.2)
    print(player.seen_pos())
    print(player.current_position)


if __name__ == '__main__':
    test()