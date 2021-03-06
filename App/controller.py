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

import config as cf
from App import model
import datetime
from datetime import timedelta, date
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion del modelo.
    """
    analyzer = model.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData(analyzer, accidentsfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    accidentsfile = cf.data_dir + accidentsfile
    input_file = csv.DictReader(open(accidentsfile,encoding="utf-8"),delimiter=",")
    for accident in input_file:
        model.addAccident(analyzer, accident)
    return analyzer

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________
def accidentsSize(analyzer):
    """
    Numero de crimenes leidos
    """
    return model.accidentsSize(analyzer)


def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer)


def indexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer)


def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)


def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)


def getAccidentsByDate(analyzer, initialDate):
    """
    Retorna el total de crimenes en un rango de fechas
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    return model.getAccidentsByDate(analyzer, initialDate.date(),
                                  )


def getAccidentsBySeverity(analyzer, initialDate, finalDate, severity):
    """
    Retorna el total de crimenes de un tipo especifico en una
    fecha determinada
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    endDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    return model.getAccidentsBySeverity(analyzer, initialDate.date(), endDate.date(), severity)


def getAccidentsBySeverity2(analyzer, initialDate,
                         severity):
    """
    Retorna el total de crimenes de un tipo especifico en una
    fecha determinada
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    return model.getAccidentsBySeverity2(analyzer, initialDate.date(),
                                      severity)
def getAccidentsByRange(analyzer, initialDate, endDate):
    """
    Retorna el total de crimenes de un tipo especifico en una
    fecha determinada
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    endDate = datetime.datetime.strptime(endDate, '%Y-%m-%d')
    print(initialDate)
    print(endDate)
    return model.getAccidentsByRange(analyzer, initialDate.date(),
                                      endDate.date())

def getMostStateAccident(analyzer, initialDate, endDate):
    """
    Retorna el total de crimenes de un tipo especifico en una
    fecha determinada
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    endDate = datetime.datetime.strptime(endDate, '%Y-%m-%d')
    return model.getMostStateAccident(analyzer, initialDate.date(),endDate.date())

def getAccidentsByHours(analyzer, initialHour, endHour, severity):
    """
    Retorna el porcentaje de los accidentes que ocurrieron respecto
    a una hora en específico
    """
    initialHour = datetime.datetime.strptime(initialHour, "%Y-%m-%d %H:%M")
    endHour = datetime.datetime.strptime(endHour, "%Y-%m-%d %H:%M")
    initialHour = aproxHour(initialHour.time())
    endHour = aproxHour(endHour.time())
    return model.getAccidentsByHours(analyzer, initialHour,
                                      endHour, severity)


def getAccidentsByHours2(analyzer, initialHour, endHour):
    """
    Retorna el porcentaje de los accidentes que ocurrieron respecto
    a una hora en específico
    """
    initialHour = datetime.datetime.strptime(initialHour, "%Y-%m-%d %H:%M")
    endHour = datetime.datetime.strptime(endHour, "%Y-%m-%d %H:%M")
    initialHour = aproxHour(initialHour.time())
    endHour = aproxHour(endHour.time())
    print(initialHour)
    print(endHour)
    return model.getAccidentsByHours2(analyzer, initialHour,
                                      endHour)


def aproxHour(datetoconvert):
    if 30 < datetoconvert.minute:
        datetoconvert=datetoconvert.replace(minute=00)
        datetoconvert = ((datetime.datetime.combine(datetime.date(1,1,1),datetoconvert) + timedelta(hours=1)).time())
    elif 30> datetoconvert.minute >15:
        datetoconvert=datetoconvert.replace(minute=30)
    elif datetoconvert.minute < 15:
        datetoconvert=datetoconvert.replace(minute=00)
    datetoconvert=datetoconvert.replace(second=0)
    return datetoconvert

def getAccidentsByArea(analyzer, latitud, longitud, radio):
    return model.getAccidentsByArea(analyzer,latitud,longitud,radio)
