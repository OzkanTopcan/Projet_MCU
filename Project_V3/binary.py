
def binairedecimal(value):
    #print(value)
    x=len(value)-2
    n=0
    res=0
    while x!=-1:
        if value[x]=="1":
            res=res+2**n
            #print(res)
        n=n+1
        x=x-1
    return res

#c = b'11100110\r\n'
#print(len(c))
#res = binairedecimal(c)
