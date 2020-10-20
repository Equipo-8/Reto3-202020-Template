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
import config
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'accidents': None,
                'severity': None
                }

    analyzer['accidents'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['severity'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    return analyzer


# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------
def addAccident(analyzer, accident):
    """
    """
    lt.addLast(analyzer['accidents'], accident)
    updateDateIndex(analyzer['severity'], accident)
    return analyzer

def updateDateIndex(map, accident):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    startTime = accident['Start_Time']
    accidentdate = datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidentdate.date())
    if entry is None:
        datentry = newDataEntry(accident)
        om.put(map, accidentdate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, accident)
    return map

def addDateIndex(datentry, accident):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstaccidents']
    lt.addLast(lst, accident)
    severityIndex = datentry['severityIndex']
    offentry = m.get(severityIndex, accident['Severity'])
    if (offentry is None):
        entry = newSeverityEntry(accident['Severity'], accident)
        lt.addLast(entry['lstseverity'], accident)
        m.put(severityIndex, accident['Severity'], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['lstseverity'], accident)
    return datentry

def newSeverityEntry(severitygrp, accident):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'Severity': None, 'lstseverity': None}
    ofentry['Severity'] = severitygrp
    ofentry['lstseverity'] = lt.newList('SINGLELINKED', compareSeveritys)
    return ofentry

def newDataEntry(accident):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'severitytIndex': None, 'lstaccidents': None}
    entry['severityIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareSeveritys)
    entry['lstaccidents'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry


def getAccidentsBySeverity(analyzer, initialDate, finalDate):
    """
    Retorna el numero de crimenes en un rago de fechas.
    """
    lst = om.values(analyzer['severity'], initialDate,finalDate)
    lstiterator = it.newIterator(lst)
    totcrimes = 0
    while (it.hasNext(lstiterator)):
        lstdate = it.next(lstiterator)
        totcrimes += lt.size(lstdate['lstaccidents'])
    accidentdate = om.get(analyzer['severity'], initialDate)
    if accidentdate['key'] is not None:
        severitymap = me.getValue(accidentdate)['severityIndex']
        numaccidents4 = m.get(severitymap,'4')
        numaccidents3 = m.get(severitymap,'3')
        numaccidents2 = m.get(severitymap,'2')
        numaccidents1 = m.get(severitymap,'1')
        dictretorno = {}
        if numaccidents4 is not None:
            dictretorno[4]=(m.size(me.getValue(numaccidents4)['lstseverity']),totcrimes)
        else:
            dictretorno[4]=(0,totcrimes)
        if numaccidents3 is not None:
            dictretorno[3]=(m.size(me.getValue(numaccidents3)['lstseverity']),totcrimes)
        else:
            dictretorno[3]=(0,totcrimes)
        if numaccidents2 is not None:
            dictretorno[2]=(m.size(me.getValue(numaccidents2)['lstseverity']),totcrimes)
        else:
            dictretorno[2]=(0,totcrimes)
        if numaccidents1 is not None:
            dictretorno[1]=(m.size(me.getValue(numaccidents1)['lstseverity']),totcrimes)
        else:
            dictretorno[1]=(0,totcrimes)
        return (dictretorno)

def getAccidentsByDate(analyzer,Date):
    lst = om.values(analyzer['severity'], Date,Date)
    lstiterator = it.newIterator(lst)
    totcrimes = 0
    while (it.hasNext(lstiterator)):
        lstdate = it.next(lstiterator)
        totcrimes += lt.size(lstdate['lstaccidents'])
    return totcrimes



def Requerimiento_2(analyzer,Date):
    x= om.minKey(analyzer['severity'])
    print(x)
    lst = om.values(analyzer['severity'],x,Date)
    list_fechas= []
    for i in range(1,6):
        x= lt.getElement(lst,i)
        accidents= x['lstaccidents']
        size= lt.size(accidents)
        for k in range(1,size):
            fecha= (lt.getElement(accidents,k))['Start_Time']
            if fecha not in list_fechas :
                list_fechas.append(fecha)
    lstiterator = it.newIterator(lst)
    totcrimes= 0
    print(list_fechas)
    print(len(list_fechas))
    while (it.hasNext(lstiterator)):
        lstdate = it.next(lstiterator)
        totcrimes += lt.size(lstdate['lstaccidents'])
    return totcrimes
        



# Funciones para agregar informacion al catalogo


# ==============================
# Funciones de consulta
# ==============================


# ==============================
# Funciones de Comparacion
# ==============================
def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1


def compareSeveritys(severity1, severity2):
    """
    Compara dos tipos de crimenes
    """
    severity = me.getKey(severity2)
    if (severity1 == severity):
        return 0
    elif (severity1 > severity):
        return 1
    else:
        return -1

def accidentsSize(analyzer):
    """
    Número de crimenes
    """
    return lt.size(analyzer['accidents'])


def indexHeight(analyzer):
    """
    Altura del arbol
    """
    return om.height(analyzer['severity'])


def indexSize(analyzer):
    """
    Numero de elementos en el indice
    """
    return om.size(analyzer['severity'])


def minKey(analyzer):
    """
    Llave mas pequena
    """
    return om.minKey(analyzer['severity'])


def maxKey(analyzer):
    """
    Llave mas grande
    """
    return om.maxKey(analyzer['severity'])
