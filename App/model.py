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
from datetime import timedelta, date
import calendar
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def datespan(startDate, endDate, delta=timedelta(minutes=30)):
    currentDate = startDate
    while currentDate < endDate:
        yield currentDate
        currentDate = (datetime.datetime.combine(datetime.date(1,1,1),currentDate) + delta).time()




# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------

def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los accidentes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas + ID

    Retorna el analizador inicializado.
    """
    analyzer = {'accidents': None,
                'dateIndex': None, 
                'hourIndex': None
                }

    analyzer['accidents'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    analyzer['hourIndex'] = om.newMap(omaptype="RBT",
                                      comparefunction=compareHours)
    return analyzer


# Funciones para agregar informacion al catalogo
def addAccident(analyzer, accident):
    """
    """
    lt.addLast(analyzer['accidents'], accident)
    updateDateIndex(analyzer['dateIndex'], accident)
    updateHourIndex(analyzer['hourIndex'], accident)
    return analyzer

def updateDateIndex(map, accident):
    """
    Se toma la fecha del accidente y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de accidentes
    y se actualiza el indice de severidad.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de severidad
    """
    occurreddate = accident['Start_Time']
    accidentdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidentdate.date())
    if entry is None:
        datentry = newDataEntry(accident)
        om.put(map, accidentdate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, accident)
    return map

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

def updateHourIndex(map, accident):
    """
    Se toma la hora del accidente y se busca si ya existe en el arbol
    dicha hora.  Si es asi, se adiciona a su lista de accidentes
    y se actualiza el indice de severidad.

    Si no se encuentra creado un nodo para esa hora en el arbol
    se crea y se actualiza el indice de tipos de severidad
    """
    occurreddate = accident['Start_Time']
    accidentdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    accidentdate = aproxHour(accidentdate.time())
    entry = om.get(map, accidentdate)
    if entry is None:
        datentry = newDataEntry(accident)
        om.put(map, accidentdate, datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, accident)
    return map

def addDateIndex(datentry, accident):
    """
    Actualiza un indice de severidad de accidentes.  Este indice tiene una lista
    de accidentes y una tabla de hash cuya llave es la severidad del accidente y
    el valor es una lista con los accidentes de dicha severidad en la fecha inicial 
    que se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstaccident']
    lt.addLast(lst, accident)
    severityIndex = datentry['severityIndex']
    seventry = m.get(severityIndex, accident['Severity'])
    if (seventry is None):
        entry = newSeverityEntry(accident['Severity'], accident)
        lt.addLast(entry['lstseverities'], accident)
        m.put(severityIndex, accident['Severity'], entry)
    else:
        entry = me.getValue(seventry)
        lt.addLast(entry['lstseverities'], accident)
    return datentry

def newDataEntry(accident):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'severityIndex': None, 'lstaccident': None}
    entry['severityIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareOffenses)
    entry['lstaccident'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def newSeverityEntry(severity, accident):
    """
    Crea una entrada en el indice por tipo de severidad, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'severity': None, 'lstseverities': None}
    ofentry['severity'] = severity
    ofentry['lstseverities'] = lt.newList('SINGLELINKED', compareOffenses)
    return ofentry


# ==============================
# Funciones de consulta
# ==============================


def accidentsSize(analyzer):
    """
    Número de crimenes
    """
    return lt.size(analyzer['accidents'])


def indexHeight(analyzer):
    """
    Altura del arbol
    """
    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):
    """
    Numero de elementos en el indice
    """
    return om.size(analyzer['dateIndex'])


def minKey(analyzer):
    """
    Llave mas pequena
    """
    return om.minKey(analyzer['dateIndex'])


def maxKey(analyzer):
    """
    Llave mas grande
    """
    return om.maxKey(analyzer['dateIndex'])


def getAccidentsByDate(analyzer, date):
    """
    Retorna el numero de crimenes en un rago de fechas.
    """
    lst = om.values(analyzer['dateIndex'], date, date)
    lstiterator = it.newIterator(lst)
    totcrimes = 0
    while (it.hasNext(lstiterator)):
        lstdate = it.next(lstiterator)
        totcrimes += lt.size(lstdate['lstaccident'])
    return totcrimes


def getAccidentsBySeverity(analyzer, initialDate, finaldate, severity):
    """
    Para una fecha determinada, retorna el numero de crimenes
    de un tipo especifico.
    """
    accidentes=0
    for x in daterange(initialDate,finaldate):
        accidentdate = om.get(analyzer['dateIndex'], x)
        if accidentdate['key'] is not None:
            offensemap = me.getValue(accidentdate)['severityIndex']
            numoffenses = m.get(offensemap, severity)
            if numoffenses is not None:
                accidentes+= m.size(me.getValue(numoffenses)['lstseverities'])
            accidentes+= 0
    return accidentes
    
def getAccidentsBySeverity2(analyzer, initialDate, severity):
    """
    Para una fecha determinada, retorna el numero de crimenes
    de un tipo especifico.
    """
    accidentdate = om.get(analyzer['dateIndex'], initialDate)
    if accidentdate['key'] is not None:
        offensemap = me.getValue(accidentdate)['severityIndex']
        numoffenses = m.get(offensemap, severity)
        if numoffenses is not None:
            return m.size(me.getValue(numoffenses)['lstseverities'])
        return 0

def getAccidentsByArea(analyzer, latitud, longitud, radio):
    central_point= (latitud**2 + longitud**2)**(1/2)
    print(central_point)
    lst = om.valueSet(analyzer['dateIndex']) #Hacemos una lista con los valores
    lstiterator = it.newIterator(lst)
    totalaccidentes = 0
    most= [0,None]
    while (it.hasNext(lstiterator)):
        lstdate = it.next(lstiterator)
        par= ((lt.getElement(lstdate['lstaccident'],1))['Start_Time']).split()
        fecha= par[0]
        size= lt.size(lstdate['lstaccident'])  
        parcial= 0 
        for i in range(1,size):
            element= lt.getElement(lstdate['lstaccident'],i)
            latitude= float(element['Start_Lat'])     
            lenght= float(element['Start_Lng'])   
            if inratio(latitude,lenght,central_point,radio):
                parcial+= 1
            else:
                parcial+= 0
        if parcial >= most[0]:
            most[0]= parcial
            most[1]= fecha
        totalaccidentes+= parcial
    return totalaccidentes, most


def inratio(latitude,lenght,rate,radio):
    if abs((latitude**2 + lenght**2)**(1/2) - rate) <= radio:
        return True
    else:
        return False



def dayoftheweek(date):
    frrr= datetime.datetime.strptime(date, '%d %m %Y')
    part= frrr.date().weekday()
    dia = calendar.day_name[part]
    return dia


def getAccidentsByRange(analyzer, initialDate, endDate):
    """
    Para un rango de fechas retorna la cantidad de accidentes
    sucedidos junto con la categoría más reportada
    """
    lst = om.values(analyzer['dateIndex'],initialDate, endDate) #Hacemos una lista con los valores
    lstiterator = it.newIterator(lst)
    totalaccidentes = 0
    most= (0,None)
    while (it.hasNext(lstiterator)):
        lstdate = it.next(lstiterator)
        z= lt.size(lstdate['lstaccident'])
        par= ((lt.getElement(lstdate['lstaccident'],1))['Start_Time']).split()
        fecha= par[0]
        if z > most[0] :
            most= (z,fecha)            
        totalaccidentes += z
    return totalaccidentes, most

def getAccidentsByHours2(analyzer, initialDate, endDate):
    """
    Para un rango de fechas retorna la cantidad de accidentes
    sucedidos junto con la categoría más reportada
    """
    lst = om.values(analyzer['hourIndex'],initialDate, endDate) #Hacemos una lista con los valores
    lstiterator = it.newIterator(lst)
    totalaccidentes = 0
    most= (0,None)
    while (it.hasNext(lstiterator)):
        lstdate = it.next(lstiterator)
        z= lt.size(lstdate['lstaccident'])
        par= ((lt.getElement(lstdate['lstaccident'],1))['Start_Time']).split()
        fecha= par[1]
        if z > most[0] :
            most= (z,fecha)            
        totalaccidentes += z
    return totalaccidentes, most

def getAccidentsByHours(analyzer, initialDate, finaldate, severity):
    """
    Para una fecha determinada, retorna el numero de crimenes
    de un tipo especifico.
    """
    accidentes=0
    for x in datespan(initialDate,finaldate,delta=timedelta(minutes=30)):
        accidentdate = om.get(analyzer['hourIndex'], x)
        if accidentdate['key'] is not None:
            offensemap = me.getValue(accidentdate)['severityIndex']
            numoffenses = m.get(offensemap, severity)
            if numoffenses is not None:
                accidentes+= m.size(me.getValue(numoffenses)['lstseverities'])
            accidentes+= 0
    return accidentes



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

def compareHours(hour1, hour2):
    """
    Compara dos horas
    """
    if hour1 == hour2:
        return 0
    elif (hour1>hour2):
        return 1
    else:
        return -1

def compareOffenses(offense1, offense2):
    """
    Compara dos tipos de crimenes
    """
    offense = me.getKey(offense2)
    if (offense1 == offense):
        return 0
    elif (offense1 > offense):
        return 1
    else:
        return -1
