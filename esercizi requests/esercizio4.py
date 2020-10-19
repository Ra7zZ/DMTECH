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
    for line in fp:
        var = line.split(",")
        x.append(var[6])
        y.append(var[1].split("-"))

print(x)
