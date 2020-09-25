def funzione(lista):
    for i in range(len(lista)):
        if(type(lista[i])==list):
            funzione(lista[i])
            lista[i].reverse()
    return

array= [11, [7,8], 33, [1,2,3,4,5,6, [1,2,3, [55,99,0,1, [23,12]]],7,8,9,1000], 0]
print(array)

array.reverse()

funzione(array)

print(array)