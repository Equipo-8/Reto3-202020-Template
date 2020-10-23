"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys
import config
from App import controller
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


accidentsfile = 'us_accidents_small.csv'

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Requerimento 1")
    print("4- Requerimento 2")
    print("5- Requerimiento 3")
    print("6- Requerimiento 4")
    print("0- Salir")
    print("*******************************************")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de accidentes ....")
        controller.loadData(cont, accidentsfile)
        print('Accidentes cargados: ' + str(controller.accidentsSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
        print('Menor Llave: ' + str(controller.minKey(cont)))
        print('Mayor Llave: ' + str(controller.maxKey(cont)))

    elif int(inputs[0]) == 3:
        print("\nRequerimiento No 1 del reto 3: ")
        print("\nBuscar por una fecha específica: ")
        initialDate = input("Ingresa la Fecha (YYYY-MM-DD): ")
        total4 = controller.getAccidentsBySeverity2(cont, initialDate, "4")
        total3 = controller.getAccidentsBySeverity2(cont, initialDate, "3")
        total2 = controller.getAccidentsBySeverity2(cont, initialDate, "2")
        total1 = controller.getAccidentsBySeverity2(cont, initialDate, "1")
        print("\nTotal de accidentes en la fecha: " + str(total4+total3+total2+total1))
        print("\nTotal de accidentes de severidad 4: "+ str(total4))
        print("\nTotal de accidentes de severidad 3: "+ str(total3))
        print("\nTotal de accidentes de severidad 2: "+ str(total2))
        print("\nTotal de accidentes de severidad 1: "+ str(total1))

    elif int(inputs[0]) == 4:
        print("\nRequerimiento No 2 del reto 3: ")
        print("\nBuscando accidentes de una fecha para atrás: ")
        finalDate = input("Rango Final (YYYY-MM-DD): ")
        total, most= controller.getAccidentsByRange(cont, str(controller.minKey(cont)), finalDate)
        print("\nEl total de accidentes de esta fecha para atrás es "+str(total))
        print("\nLa fecha con un mayor numero de accidentes en este rango de fecha es " + str(most[1] + " con un numero de accidentes igual a : " +str(most[0])))
        
    elif int(inputs[0]) == 5:
        print("\nBuscando accidentes por severidad en la fecha: ")
        initialDate = input("Ingresa la Fecha (YYYY-MM-DD): ")
        finalDate = input("Rango Final (YYYY-MM-DD): ")
        total4 = controller.getAccidentsBySeverity(cont, initialDate, finalDate, "4")
        total3 = controller.getAccidentsBySeverity(cont, initialDate, finalDate, "3")
        total2 = controller.getAccidentsBySeverity(cont, initialDate, finalDate, "2")
        total1 = controller.getAccidentsBySeverity(cont, initialDate, finalDate, "1")
        print("\nTotal de accidentes en la fecha: " + str(total4+total3+total2+total1))
        print("\nTotal de accidentes de severidad 4: "+ str(total4))
        print("\nTotal de accidentes de severidad 3: "+ str(total3))
        print("\nTotal de accidentes de severidad 2: "+ str(total2))
        print("\nTotal de accidentes de severidad 1: "+ str(total1))
    elif int(inputs[0]) == 6:
        print("\nRequerimiento No 4 del reto 3: ")
        initialDate = input("Rango Inicial (YYYY-MM-DD): ")
        finalDate = input("Rango Final (YYYY-MM-DD): ")
        total = controller.getMostStateAccident(cont, initialDate, finalDate, "4")
    elif int(inputs[0]) == 7:
        print("\nRequerimiento No 5 del reto 3: ")
        initialDate = input("Hora Inicial (HH:MM): ")
        initialDate = str(controller.minKey(cont))+" "+initialDate
        finalDate = input("Hora Final (HH:MM): ")
        finalDate = str(controller.maxKey(cont))+" "+finalDate
        #total = controller.getAccidentsByHours(cont, initialDate, finalDate,"4")
        total2 = controller.getAccidentsByHours2(cont, initialDate, finalDate)
        #print(total)
        print(total2)
    else:
        sys.exit(0)
sys.exit(0)
