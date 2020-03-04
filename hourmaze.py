import sys
import os
import subprocess
import io

NCOL = 0
NFIL = 0

#In -> row, colum y value para una determinada casilla
#Out -> numero de la proposicion que representa si (val) está en (row, col)
def get_proposition(row, col, val):
    #El numero de casillas completadas es el numero de casillas recorridas menos
    #la casilla en la que se encuentra
    casillas_completas = (NCOL*(row-1)) + col -1
    #El valor será el de las casillas completas * 12 + valor casilla que se encuentra
    valor = casillas_completas*12+val
    return valor

#In -> numero de la proposicion
#Out -> row, column y val en (row, col) a los que representa 
def get_position(prop):
    n_casillas = 0 #Suponemos que el numero de casillas completas es 0
    n_fila = 1 #Suponemos que se encuentra en la primera fila
    n_columna = 1 #Suponemos que se encuentra en la primera columna

    #Calculamos el numero de casillas completas
    while (prop>12):
        prop = prop - 12
        n_casillas = n_casillas + 1
        pass
    #Calculamos el numero de filas completas
    while (n_casillas > NCOL):
        n_fila = n_fila + 1
        n_casillas = n_casillas - NCOL
        pass
    n_columna = n_casillas

    #Ahora en n_columna tenemos el indice de la ultima columna completa del elemento
    #Ahora en n_fila tenemos el indice de la ultima fila completa del elemento
    #Tenemos en 'prop' el valor de la casilla en la que se encuentra
    
    #Miramos si queda algo en prop, es decir, si hay otra casilla
    if (prop>0):
        #Si nos encontramos en la ultima columna del tablero
        if (n_columna == NCOL):
            n_columna = 1
            n_fila = n_fila + 1
        #Si no nos encontramos en la ultima columna, simplemente añadimos 1 columna
        else:
            n_columna = n_columna + 1
    
    return (n_fila, n_columna, prop)


def get_direcciones(tablero, posicion):
    direcciones = {'up':[0,1], 'down':[0,-1], 'right':[1,0],'left':[-1,0]}
    print("[*] Computing all posible directions for",posicion)
    result = {}
    #Para todas las direcciones que existen
    for direccion, vector in direcciones.items():
        #Calculamos los movimientos de la posicion dada
        new_position = [(posicion[0] + vector[0]),(posicion[1] + vector[1])]
        new_pos_row = new_position[0]
        new_pos_col = new_position[1]
        #Vemos si la posicion tras el movimiento es valida
        if not (new_pos_row > NFIL or new_pos_row <= 0 or new_pos_col > NCOL or new_pos_col <= 0):
            #Si es valida la añadimos al resultado
            result[direccion]=new_position
    return result

def main(argv):
    if (len(argv) != 2):
        print("Incorrect number of arguments")
    else:
        filename = argv[1]
        table_file = open(filename,"r");
        fo = open("clasp.txt","w");
        data = io.StringIO("")
        clausulas = 0

        global NCOL
        global NFIL
        NCOL = int(table_file.read(1))
        if (table_file.read(1) != '\n'):
                print("Parsing error")
                return -1
        NFIL = int(table_file.read(1))
        if (table_file.read(1) != '\n'):
                print("Parsing error")
                return -1

        print("[*] Starting HourMaze for cols =",NCOL,"rows =",NFIL)
        tablero = [line.split() for line in table_file]
        
        #Diccionario de direcciones
        direcciones = {'up':[0,1], 'down':[0,-1], 'right':[1,0],'left':[-1,0]}
        print(direcciones['up'])

        #Parseamos el tablero
        fila = 1
        for row in tablero:
            columna = 1
            for element in row:
                #Si el elemento encontrado es un numero significa que hay un valor fijo 
                if (element.isdigit()):
                    element = int(element)
                    #Marcamos como TRUE la proposición de que en esa casilla está el numero indicado
                    #Marcamos como FALSE las proposiciones de que en esa casilla hay cualquier otro numero
                    for i in range(1,13):
                        if (element != i):
                            data.write("-{} 0".format(get_proposition(fila, columna, i)))
                        else:
                            data.write("{} 0".format(get_proposition(fila, columna, i)))
                        
                        data.write("\n")
                        clausulas+=1

                #Si el elemento encontrado no es un numero significa que hay 'x', ' ', '|' o '-'
                else:
                    vecinos = get_direcciones(tablero, [fila, columna])
                    #Para cada uno de los vecinos del elemento
                    for direccion, vecino in vecinos.items():
                        #"SI EL VALOR DE MI VECINO ES 1 ENTOINCES MI VALOR ES 2"
                        #CNF: (valor 1 en vecino) -> (valor es 2) = -(valor 1 vecino) v -(valor 2) = -(valor 1 vecino) -(valor 2)
                        for i in range(1,13):
                            print("Indicando la restriccion para n =",i,"en",[fila, columna],"en direccion",direccion,":")
                            proposicion_vecino = get_proposition(vecino[0], vecino[1], i)
                            proposicion_elemento = get_proposition(fila, columna,((i+1)%12))
                            print("Para valor de",get_position(proposicion_elemento),"ponemos la restriccion de",get_position(proposicion_vecino))

                            data.write("c [*] Indicando la restriccion para n = {} en {} en direccion {}: ".format(i, [fila,columna],direccion))
                            data.write("\n")

                            data.write("-{} ".format(proposicion_vecino))
                            data.write("-{} ".format(proposicion_elemento))
                            data.write("\n")
                            clausulas+=1
                    
                columna +=1
            fila += 1
        
        fo.write("p cnf {} {}\n".format(NCOL*NFIL*12,clausulas));
        fo.write(data.getvalue())
        fo.close()
        table_file.close()


if __name__ == "__main__": 
    main(sys.argv)
