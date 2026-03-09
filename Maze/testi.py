from map import Map
#W W W
#W p .
#W W W
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
        
        self.view = (self.view - 180) % 360                                            #look left
        spot= find_spot(self.view, self.current_position)
        if self.current_map.check_coordinate(spot[0],spot[1]) == "Path":
            self.current_position = spot
            return None
        
        self.view = (self.view + 90) % 360                                             #look straight
        spot= find_spot(self.view, self.current_position)
        if self.current_map.check_coordinate(spot[0],spot[1]) == "Path":
            self.current_position = spot
            return None
        
        self.view = (self.view - 180) % 360                                             #look back
        spot= find_spot(self.view, self.current_position)
        if self.current_map.check_coordinate(spot[0],spot[1]) == "Path":
            self.current_position = spot
            return None

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


def main():
    map_test= Map(r"SWENG\Maze\mazes\test-maze.txt")
    player = Player(map_test)
    print(player.position())
    player.move()
    print(player.position())


    


main()
