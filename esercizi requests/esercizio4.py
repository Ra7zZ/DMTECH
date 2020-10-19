import requests
import matplotlib
import csv

response = requests.get("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv")
#print(response.text)
File = open("covid.csv", "w")
File.write(response.text)
File.close()

x = []
y = []


with open("covid.csv", "r") as fp:
    row_count = sum(1 for row in fp)
    for i = 1 in fp.r:
        var = line.split(",")
        if(line != "totale_positivi"):
            y.append(float(var[6]))
            x.append(var[1])


#print(x)
