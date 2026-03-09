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
    size = testmap.size()
    start = testmap.get_start()
    finish = testmap.get_finish()
    coins = testmap.get_coins()
    return size,start,finish,coins

if __name__ == '__main__':
    print(self_test())
