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

def main(argv):
    if (len(argv) != 2):
        print("Incorrect number of arguments")
    else:
        filename = argv[1]
        fi = open(filename,"r");
        fo = open("clasp.txt","w");

        global NCOL
        global NFIL
        NCOL = int(fi.read(1))
        if (fi.read(1) != '\n'):
                print("Parsing error")
                return -1
        NFIL = int(fi.read(1))
        if (fi.read(1) != '\n'):
                print("Parsing error")
                return -1

        cmap = [[None for x in range(NFIL+NFIL-1)] for y in range(NCOL+NCOL-1)]
	

        i = 0
        j = 0
        lines = fi.readlines()
        for line in lines:
            for ch in line:
                if (ch != '\n'):
                    cmap[i][j] = ch
                    i = i + 1
            i = 0
            j = j + 1

        data = io.StringIO("")
        clausules = 0
        for y in range(0,NFIL):
            for x in range(0,NCOL):
                ch = cmap[x*2][y*2]
                print(ch,end='')
                if ch.isdigit():
                    data.write("c ----COMENTARIO---- VALOR FIJO casilla {},{}\n".format(x+1,y+1))
                    for i in range(1,13):
                        if int(ch) != i:
                            data.write("-{} 0".format(get_proposition(y+1,x+1,i)));
                            #data.write(" #VALOR FIJO");
                            data.write("\n");
                            clausules += 1
                        else:
                            data.write("{} 0".format(get_proposition(y+1,x+1,i)));
                            #data.write(" #VALOR FIJO");
                            data.write("\n");
                            clausules += 1
                else:
                    for ixy in [[-1,0],[1,0],[0,-1],[0,1]]: #Recorrer los vecinos
                        #Descartamos los vecinos de fuera de la cuadricula
                        if ((x+1+ixy[0] != 0) and (x+1+ixy[0] != NCOL+1) and (y+1+ixy[1] != 0) and (y+1+ixy[1] != NFIL+1)): 
                            data.write("c ----COMENTARIO---- VALOR DE {},{} RESPECTO A {},{}\n".format(x+1,y+1,x+1+ixy[0],y+1+ixy[1]))
                            for i in range(1,13):
                                #CNF: (valor 1 en vecino) -> (valor es 2) = -(valor 1 vecino) v -(valor 2) = -(valor 1 vecino) -(valor 2)
                                if (i-1 != 0):
                                    data.write("{} ".format(get_proposition(y+1+ixy[1],x+1+ixy[0],i-1)))
                                if (i+1 != 13):
                                    data.write("{} ".format(get_proposition(y+1+ixy[1],x+1+ixy[0],i+1)))
                                data.write("-{} 0 ".format(get_proposition(y+1,x+1,i)))
                                data.write("\n")
                                clausules += 1
            print("\n",end='')

        print("\n")
        fo.write("c numero de atomos = columnas*filas*12\n");
        fo.write("p cnf {} {}\n".format(NCOL*NFIL*12,clausules));
        fo.write(data.getvalue())
        fo.close()
        fi.close()
        try:
            os.remove("sol.txt")
        except:
            pass
        os.system("clasp clasp.txt >> sol.txt")

        #Ahora se lee la solucion
        fs = open("sol.txt","r");
        lines = fs.readlines()
        smap = cmap
        for line in lines:
            if (line[0] == 'v'):
                for proposition in line[1:].split(' '):
                    try:
                        if (int(proposition) > 0):
                            a = get_position(int(proposition))
                            print(proposition,": ",a)
                            smap[(a[1]-1)*2][(a[0]-1)*2] = a[2]
                    except:
                        pass

        fs.close()
        print("\n")
        for y in range(0,NFIL):
            for x in range(0,NCOL):
                ch = smap[x*2][y*2]
                print(ch,end='')
            print("\n",end='')



if __name__ == "__main__": 
    main(sys.argv)
