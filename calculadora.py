def calcula(x):
    resultado = 0

    valor = x.split(" ")
    sem_espaço = ''.join(valor)

    soma = sem_espaço.split("+")

    for i in soma:
        if i == '':
            pass
        elif '-' in i:
            sub = i.split("-")
            for e in sub:
                if e == '':
                    pass 
                elif e == sub[0]:
                    resultado+=int(e)
                else:
                    resultado-=int(e)
        else:
            resultado+=int(i)

    return resultado

print(calcula("     -110+ 798     +435   -     123    "))