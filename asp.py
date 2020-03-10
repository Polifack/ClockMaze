import sys
import os
import io
import math


def get_neighbours(i, j, tablero, rows, cols):
    neighbours = []
    #check up
    if (not((i-2)<0)and (tablero[i-1][j]!='-')):

        neighbours.append((i-2,j))
    #check down
    if (not((i+2)>rows)and (tablero[i+1][j]!='-')):

        neighbours.append((i+2,j))
    #check left
    if (not((j-2)<0) and (tablero[i][j-1]!='|')):

        neighbours.append((i,j-2))
    #check right
    if (not((j+2)>cols) and (tablero[i][j+1]!='|')):

        neighbours.append((i,j+2))

    return neighbours

#traduce una posicion de un nodo (element) del grafo a una posicion del tablero
def graph_to_map(element, tablero, rows, cols):
    n_fila = 1 #Suponemos que se encuentra en la primera fila
    n_columna = 1 #Suponemos que se encuentra en la primera columna
    #Calculamos el numero de filas completas
    n_casilla = 1
    while(n_casilla<element):
        n_casilla+=1
        n_columna+=1
        if (n_casilla%cols==1):
            n_fila+=1
            n_columna=1
    n_fila_tablero = (n_fila-1)*2;
    n_columna_tablero = (n_columna-1)*2;
    return(tablero[n_fila_tablero][n_columna_tablero], n_fila_tablero,n_columna_tablero)

#traduce una posicion del mapa a un nodo del grafo
def map_to_graph(row,col,nrows,ncols):
    r=(row/2)*ncols
    c=(col/2)+1
    p=r+c
    return p

def create_map(fi):
    ncols = int(fi.read(1))
    if (fi.read(1) != '\n'):
            print("Parsing error")
            return -1
    nrows = int(fi.read(1))
    if (fi.read(1) != '\n'):
            print("Parsing error")
            return -1

    lines = fi.readlines()
    tablero = []
    graph = []
    i = 1
    nrow = 1
    for line in lines:
        row = []
        grow = []
        for ch in line:
            if (ch != '\n'):
                row.append(ch)
                if (ch!=' ' and ch!='-' and ch!='|'):
                    grow.append(i)
                    i+=1
        nrow+=1
        if (nrow%2==0):
            graph.append(grow)
        tablero.append(row)
    return (nrows, ncols, tablero, graph)

def create_graph(fi):
    r,c,t,g = create_map(fi)
    print(t)
    vertex = []
    edges = []
    for row in g:
        for e in row:
            vertex.append(e)
            element, fila, columna = graph_to_map(e, t, r, c)
            neighbours = get_neighbours(fila, columna, t, r, c)
            for n in neighbours:
                fila_vecino, columna_vecino = n
                nodo_vecino = map_to_graph(fila_vecino,columna_vecino,r,c)
                edges.append((e,nodo_vecino))
    i = 0
    j = 0

    fixed_elements = []
    for row in t:
        i+=1
        for ch in row:
            if (ch.isdigit()):
                node = map_to_graph(i,j,r,c)
                fixed_elements.append((node, int(ch)))
            j+=1

    n_elements = float(r*c)
    n_rep = int(math.ceil(n_elements/12))
    print("numero repeticiones = ",n_rep)

    send_to_file(vertex,edges,fixed_elements,n_rep)
    
def send_to_file(vertex, edges, fixed_elements, n_repeticiones):
    f = open("clingo.txt","w");
    f.write("hours(1..12).\n")
    for v in vertex:
        f.write("vtx("+str(v)+").\n")
    for (v1,v2) in edges:
        f.write("edge("+str(v1)+","+str(v2)+").\n")
    for (n, e) in fixed_elements:
        f.write("element("+str(n)+","+str(e)+").\n")
    
    f.write(str(len(vertex))+"{element(X,V) : vtx(X), hours(V)}.\n")
    f.write(":-element(X, V), element(X, W), W!=V.\n")
    f.write("adj(X,Y) :- hours(X), hours(Y), |X-Y|==1.\n")
    f.write(":-element(X,V), element(Y, W), edge(X, Y), not adj(W,V).\n")
    f.write("#show element/2.\n")
    #f.write( Condicion de que el numero de veces que se pone cada elemento no sea mayor que n_repeticiones )
    f.close()

    get_answer()

def get_answer():
    try:
        os.remove("sol_clingo.txt")
    except:
        pass
    os.system("clingo clingo.txt >> sol_clingo.txt")

    f = open("sol_clingo.txt","r")
    lines = f.readlines()
    for line in lines:
        if line[0] == 'e':
            print(line)

def main(argv):
    if (len(argv) != 2):
        print("Incorrect number of arguments")
    else:
        filename = argv[1]
        table_file = open(filename,"r")
        create_graph(table_file)

if __name__ == "__main__": 
    main(sys.argv)
