def is_balanced(s):
    lista=[]
    for i in s:
        if i=="(":
            lista.append(1)
            #print(lista)
        elif i==")":
            if (len(lista)>0) and (lista[-1]==1):
                lista=lista[:-1]
                #print(lista)
            else:
                return False
    if len(lista)==0:
        return True
    else:
        return False

s="ciao"
print(is_balanced(s))

s="(ok)"
print(is_balanced(s))

s="(2(3+7))"
print(is_balanced(s))

s="(2(3+7)) + (3-2)"
print(is_balanced(s))

s="("
print(is_balanced(s))

s=")("
print(is_balanced(s))

s="((()()"
print(is_balanced(s))
