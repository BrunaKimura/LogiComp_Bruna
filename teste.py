lista= ["me", "print", "por", "favor"]


with open ("output.txt", 'w') as file:
    for linha in lista:
        file.write(linha + "\n") 