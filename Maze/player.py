from map import Map

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


def test():

    #W W W
    #W p .
    #W W W

    current_map = (("Wall", "Wall" , "Wall") , ("Wall","Path", "Path") , ("Wall", "Wall" , "Wall"))
    current_position = (1,1)
    visited_position= set()
    view = 0                           #start looking down

    def position():  
        return current_position

    def move(view,current_position):
        spot= (0,0)
        visited_position.add(current_position)

        view = (view + 90) % 360  
        print(view)                                            #look right
        spot= find_spot(view, current_position)
        if check_coordinate(spot[0],spot[1]) == "Path":
            current_position = spot
            return current_position
        
        view = (view - 180) % 360                              #look left
        print(view)                                       
        spot= find_spot(view, current_position)
        if check_coordinate(spot[0],spot[1]) == "Path":
            current_position = spot
            return current_position
        
        view = (view + 90) % 360                                             #look straight
        print(view)                                       
        spot= find_spot(view, current_position)
        if check_coordinate(spot[0],spot[1]) == "Path":
            current_position = spot
            return current_position
        
        view = (view - 180) % 360                                             #look back
        print(view)                                       
        spot= find_spot(view, current_position)
        if check_coordinate(spot[0],spot[1]) == "Path":
            current_position = spot
            return current_position

    def seen_pos():

    def check_coordinate(x,y):
        row = current_map[y]
        place = row[x]
        if place == "Path": return "Path"
        else: return "Wall"


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
        print(current_position)
        print(move(view, current_position))


    main()
