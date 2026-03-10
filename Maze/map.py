"""
Geschrieben von Marvin Horn
"""

class Map:
    
    def __init__(self, filepath) -> None:
        self.gridlist = []
        self.start = ()
        self.finish = ()
        self.coins = []
        
        with open(filepath,'r') as file:
            file_data: list[str] = file.read().splitlines()

        for y, row in enumerate(file_data):
            row_clean = row.strip()
            rowlist = []
            for x, char in enumerate(row_clean):
                if any(["." in data_row for data_row in file_data]):
                
                    if char == ".":
                        rowlist.append("Path")
                    elif char == "W":
                        rowlist.append("Wall")
                    elif char == "S":
                        rowlist.append("Path")
                        self.start = (x,y)
                    elif char == "Z":
                        rowlist.append("Path")
                        self.finish = (x,y)
                    elif char.isdigit():
                        rowlist.append("Path")
                        self.coins.append(((x,y),int(char)))
                else:
                
                    if char == "W":
                        rowlist.append("Path")
                    elif char == "X":
                        rowlist.append("Wall")
                    elif char == "S":
                        rowlist.append("Path")
                        self.start = (x,y)
                    elif char == "Z":
                        rowlist.append("Path")
                        self.finish = (x,y)
                    elif char.isdigit():
                        rowlist.append("Path")
                        self.coins.append(((x,y),int(char)))
            self.gridlist.append(rowlist)


    def size(self):
        return (len(self.gridlist[0]),len(self.gridlist))

    def check_coordinates(self,position):
        x= position[0]
        y= position[1]
        if x < 0 or x >= len(self.gridlist[0]) or y < 0 or y >= len(self.gridlist):
            return "Wall"
        return self.gridlist[y][x]
    
    def get_start(self):
        return self.start
    
    def get_finish(self):
        return self.finish
    
    def get_coins(self):
        return self.coins
    
def self_test():
    testmap = Map("./Maze/mazes/test-maze.txt")

    grid = testmap.gridlist
    assert grid == [['Path', 'Path', 'Wall'], ['Wall', 'Path', 'Wall'], ['Path', 'Path', 'Wall']]

    size = testmap.size()
    assert size == (3,3)

    start = testmap.get_start()
    assert start == (0,0)
    finish = testmap.get_finish()
    assert finish == (0,2)

    coins = testmap.get_coins()
    assert coins == [((1, 1), 1)]

    checkedcords = testmap.check_coordinates((2,2))
    assert checkedcords == "Wall"
    

if __name__ == '__main__':
    self_test()