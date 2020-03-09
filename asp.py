import sys
import os
import io

def get_neighbours(i, j, tablero, rows, cols):
    neighbours = []
    #check up
    if not ((i-1)<0):
        up = tablero[i-1][j]
        neighbours.append(up)
    #check down
    if not((i+1)>rows):
        down = tablero[i+1][j]
        neighbours.append(down)
    #check left
    if not((j-1)<0):
        left = tablero[i][j-1]
        neighbours.append(left)
    #check right
    if not((j+1)>0):
        right = tablero[i][j+1]
        neighbours.append(right)

    return neighbours

def create_graph(tablero):
    vertex = []
    edges = []

    cols = tablero[0]
    rows = tablero[1]

    print(rows, cols)

    vertex_counter = 0
    for i in range(2, len(tablero)):
        for j in range(0, len(tablero[i])):
            vertex_counter += 1
            vertex_value = None
            
            print("Adding vertex ",i-2,j,"at",vertex_counter)
            if(tablero[i][j].isdigit()):
                vertex_value = tablero[i-2][j]

            vertex.append((vertex_counter,vertex_value))

            neighbours = get_neighbours(i-2,j, tablero, rows, cols)
            print(neighbours)





def main(argv):
    if (len(argv) != 2):
        print("Incorrect number of arguments")
    else:
        filename = argv[1]
        table_file = open(filename,"r")

        tablero = [line.split() for line in table_file]
        create_graph(tablero)

if __name__ == "__main__": 
    main(sys.argv)
