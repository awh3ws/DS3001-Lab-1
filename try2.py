import pandas as pd
import networkx as nx
import random
from numpy import transpose


df = pd.read_csv ('county_adjacencies.csv')
noDel = df

totPop = 0 #calculates total population
for i in range (0, len(df.Population2022)):
  totPop += df.Population2022[i]
  
districts = [[0]*132 for i in range(11)] #initializes voting districts array

adjac = [[0]*10 for i in range(10)] #Generates adjacency lists
trueAdjac = [[0]*133 for i in range(10)]

adjac[0] = df.N1
adjac[1] = df.N2
adjac[2] = df.N3
adjac[3] = df.N4
adjac[4] = df.N5
adjac[5] = df.N6
adjac[6] = df.N7
adjac[7] = df.N8
adjac[8] = df.N9
adjac[9] = df.N10

for i in range (len(adjac)):
    for j in range (len(adjac[i])):
        if str(adjac[i][j]) == "nan":
            adjac[i][j] = "na"

for i in range (len(adjac)):
    for j in range (len(adjac[i])):
        trueAdjac[i][j] = adjac[i][j]
        
pops = [0,0,0,0,0,0,0,0,0,0,0]

def removeCounty(num):
  for j in range (0, len(df.County)): #removes seed counties from adjacency list
      if df.N1[j] == df.County[num]:
        df.loc[j, 'N1'] = "na"
      if df.N2[j] == df.County[num]:
        df.loc[j, 'N2'] = "na"
      if df.N3[j] == df.County[num]:
        df.loc[j, 'N3'] = "na"
      if df.N4[j] == df.County[num]:
        df.loc[j, 'N4'] = "na"
      if df.N5[j] == df.County[num]:
        df.loc[j, 'N5'] = "na"
      if df.N6[j] == df.County[num]:
        df.loc[j, 'N6'] = "na"
      if df.N7[j] == df.County[num]:
        df.loc[j, 'N7'] = "na"
      if df.N8[j] == df.County[num]:
        df.loc[j, 'N8'] = "na"
      if df.N9[j] == df.County[num]:
        df.loc[j, 'N9'] = "na"
      if df.N10[j] == df.County[num]:
        df.loc[j, 'N10'] = "na"

randNum = 0 #generates seed counties
for i in range (0, 11):
  randNum = random.randint(0, 132)
  districts[i][0] = df.loc[randNum, 'County']
  pops[i] = df.loc[randNum, 'Population2022']
  removeCounty(randNum)
  
  
def nextToAdd(): #Function to change, currently just chooses least populated
    maxPriority = pops.index(min(pops))
    return maxPriority


def allna(): #Determines if all counties have been placed
    for i in range (len(adjac)):
        for j in range (len(adjac[i])):
            if len(adjac[i][j]) > 2:
                return False
    return True

def getPop(county):
    counties = df.County.values.flatten().tolist()
    indexOfCounty = counties.index(county)
    return df.Population2022[indexOfCounty]

def insertCounty(county, row):
    for i in range (0, len(districts[row])):
        if districts[row][i] == 0:
            districts[row][i] = county
            break

def chooseCounty(nexDistrict):
    countyToNeighbor = ""
    col = 0
    
    while len(str(countyToNeighbor)) < 3:
        col = random.randint(0, len(districts[nexDistrict]) - 1)
        countyToNeighbor = districts[nexDistrict][col]
    
    return countyToNeighbor
   
def isValidRemove(county):
    d = []
    
    for i in range (0, len(districts)):
          if county in districts[i]:
                d = districts[i]
    
    distGraph = nx.Graph()
      
    for i in range (0,len(d)):
        if d[i] != 0:
          distGraph.add_node(d[i])
      
    if len(d) == 0:
          return False
    for i in range (0, len(d)):
          for j in range (0, len(trueAdjac)):
                for k in range (0, len(trueAdjac[j])):
                  if d[i] == trueAdjac[j][k]:
                        connectTo = counties[k] #not properly created edges
                        if connectTo in d:
                          distGraph.add_edge(d[i], connectTo)
      
    
    distGraph.remove_node(county)
    if len(list(distGraph.nodes)) == 1:
        return False
    if nx.is_connected(distGraph):
        return True

    return False  
      

def flip(nexDistrict):
    countyToNeighbor = chooseCounty(nexDistrict)
    
    adjToCounty = ""
    numChecks = 0
    while len(adjToCounty) < 3:
        if numChecks >= 15:
            countyToNeighbor = chooseCounty(nexDistrict)
            numChecks = 0
            
        adjToCounty = trueAdjac[random.randint(0,9)][counties.index(countyToNeighbor)]
        while adjToCounty == "na":
            adjToCounty = trueAdjac[random.randint(0,9)][counties.index(countyToNeighbor)]
        if adjToCounty in districts[nexDistrict]:
            adjToCounty = ""
            numChecks += 1
        elif not isValidRemove(adjToCounty):
            adjToCounty = ""
            numChecks += 1

    for i in range (0, len(districts)):
        for j in range (0, len(districts[i])):
            if adjToCounty == districts[i][j]:
                districts[i][j] = 0
                pops[i] -= getPop(adjToCounty)
            

    pops[nexDistrict] += getPop(adjToCounty)
    insertCounty(adjToCounty, nexDistrict)
    
tot = 11
counties = df.County.values.flatten().tolist()
while not allna():
    nextDisctrict = nextToAdd()
    maxPop = 0
    maxIndex = 0
    maxRow = 0
    for i in range (len(districts[nextDisctrict])):
        if districts[nextDisctrict][i] == 0:
            break
        row = counties.index(districts[nextDisctrict][i])
        for j in range (0, 10):
            if adjac[j][row] != "na":
                if maxPop < getPop(adjac[j][row]): #currently choosing to add the county adjacent to the district with the largest population
                    maxPop = getPop(adjac[j][row])
                    maxIndex = j
                    maxRow = row
    
    if adjac[maxIndex][maxRow] == "na":
        flip(nextDisctrict)
    
    else:
        tot += 1
        insertCounty(adjac[maxIndex][maxRow], nextDisctrict)
        pops[nextDisctrict] += getPop(adjac[maxIndex][maxRow])
        toRem = counties.index(adjac[maxIndex][maxRow])
        removeCounty(toRem)
    
print(districts)