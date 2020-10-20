import requests
import matplotlib.pyplot as plt
from dateutil import parser

response = requests.get("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv")
#print(response.text)
File = open("covid.csv", "w")
File.write(response.text)
File.close()

x = []
y = []


with open("covid.csv", "r") as fp:
    #row_count = sum(1 for row in fp)
    for line in fp:
        var = line.split(",")
        if(var[6] != "totale_positivi"):
            y.append(float(var[6]))
        
        if(var[0] != "data"):
            #print(parser.parse(var[0]))
            data = var[0].split("T")
            giorno = data[0]
            #print(giorno)
            x.append(giorno)

#datetime has no fromisoformat member
#parser has no isoparse module
#print(y)
#print(x)

plt.plot(x,y)
plt.ylabel('totale_positivi')
plt.xlabel('data')
plt.show()
