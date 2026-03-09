class Map:
    
    def __init__(self, filepath) -> None:
        self.gridlist = []
        self.start = ()
        self.finish = ()
        self.coins = []
        
        with open(filepath,'r') as file:
            for y, row in enumerate(file):
                row_clean = row.strip()
                rowlist = []
                if any(["." in data_row for data_row in file]):
                    for x, char in enumerate(row_clean):
                        if char == ".":
                            rowlist.append("Path")
                        elif char =="W":
                            rowlist.append("Wall")
                        elif char == "S":
                            rowlist.append("Path")
                            self.start = (x,y)
                        elif char == "Z":
                            rowlist.append("Path")
                            self.finish = (x,y)
                        elif char.isdigit():
                            rowlist.append("Path")
                            self.coins.append((x,y,int(char)))
                    self.gridlist.append(rowlist)
                else:
                    for x, char in enumerate(row_clean):
                        if char == "W":
                            rowlist.append("Path")
                        elif char =="X":
                            rowlist.append("Wall")
                        elif char == "S":
                            rowlist.append("Path")
                            self.start = (x,y)
                        elif char == "Z":
                            rowlist.append("Path")
                            self.finish = (x,y)
                        elif char.isdigit():
                            rowlist.append("Path")
                            self.coins.append((x,y,int(char)))
                    self.gridlist.append(rowlist)


    def size(self):
        return (len(self.gridlist[0]),len(self.gridlist))

    def check_coordinate(self,x,y):
        return self.gridlist[y][x]
    
    def get_start(self):
        return self.start
    
    def get_finish(self):
        return self.finish
    
    def get_coins(self):
        return self.coins
        

def self_test():
    testmap = Map("./mazes/test-maze.txt")
    grid = testmap.gridlist
    size = testmap.size()
    start = testmap.get_start()
    finish = testmap.get_finish()
    coins = testmap.get_coins()
    checkedcords = testmap.check_coordinate(2,2)
    return size,checkedcords,start,finish,coins,grid

if __name__ == '__main__':
    print(self_test())
