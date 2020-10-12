def recursive_reverse_list(arrayVecchio):

    generated=[]
    for i in range(len(arrayVecchio)-1, -1, -1):
        if(type(arrayVecchio[i])==int):
            generated.append(arrayVecchio[i])
        else:
            generated.append(recursive_reverse_list(arrayVecchio[i]))
    return generated

array= [11, [7,8], 33, [1,2,3,4,5,6, [1,2,3, [55,99,0,1, [23,12]]],7,8,9,1000], 0]

nuovo = recursive_reverse_list(array)

print("array nuovo\n"+str(nuovo))
