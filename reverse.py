from copy import deepcopy
def recursive_reverse_list(lista):
    for var in lista:
        if(type(var)==list):
            recursive_reverse_list(var)
            var.reverse()
    return

array= [11, [7,8], 33, [1,2,3,4,5,6, [1,2,3, [55,99,0,1, [23,12]]],7,8,9,1000], 0]

print("Originale prima del reverse:\n"+str(array))

arrayCopia=deepcopy(array)

arrayCopia.reverse()

recursive_reverse_list(arrayCopia)

print("Originale dopo il reverse:\n"+str(array))
print("Array dopo reverse:\n"+str(arrayCopia))
