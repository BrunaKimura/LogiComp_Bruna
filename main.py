class Token:
    def __init__(self, t, v):
        self.type = t
        self.value = v

class Tokenizer:
    def __init__(self, o):
        self.origin = o
        self.position = 0
        self.actual = self.selectNext()

    def selectNext(self):
        word = ""

        while self.position<len(self.origin) and self.origin[self.position].isspace():
            self.position+=1

        if self.position == len(self.origin):
            new_token = Token("eof", "")
            word = 'eof'
            self.actual = new_token

        while self.position<len(self.origin) and self.origin[self.position].isdigit():
            word+=self.origin[self.position]
            self.position+=1

        if word == 'eof':
            pass

        elif word == "":
            if self.origin[self.position] == '+':
                new_token = Token("plus", "+")
                self.actual = new_token
                self.position+=1

            elif self.origin[self.position] == '-':
                new_token = Token("minus", "-")
                self.actual = new_token
                self.position+=1

            elif self.origin[self.position] == '*':
                new_token = Token("mult", "*")
                self.actual = new_token
                self.position+=1

            elif self.origin[self.position] == '/':
                new_token = Token("div", "/")
                self.actual = new_token
                self.position+=1

            else:
                raise ValueError("token inexistente")
        else:
            new_token = Token("int",int(word))
            self.actual = new_token

        return new_token


class Parser:
    
    def parserTerm():
        if Parser.tokens.actual.type == 'int':
            resultado = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            while Parser.tokens.actual.type == 'mult' or Parser.tokens.actual.type == 'div':
                if Parser.tokens.actual.type == 'mult':
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == 'int':
                        resultado *= Parser.tokens.actual.value
                    else:
                        raise ValueError("erro ao multiplicar")
                elif Parser.tokens.actual.type == 'div':
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == 'int':
                        resultado //= Parser.tokens.actual.value
                    else:
                        raise ValueError("erro ao dividir")
                Parser.tokens.selectNext()
        else:
            raise ValueError("erro: expressão iniciada em 0")

        return resultado

    def parserExpression():
        resultado = Parser.parserTerm()
        while Parser.tokens.actual.type == 'plus' or Parser.tokens.actual.type == 'minus':
            if Parser.tokens.actual.type == 'plus':
                Parser.tokens.selectNext()
                resultado+=Parser.parserTerm()
            if Parser.tokens.actual.type == 'minus':
                Parser.tokens.selectNext()
                resultado-=Parser.parserTerm()
            
        return resultado


    def run(code):
        Parser.tokens = Tokenizer(code)
        a = Parser.parserExpression()
        if Parser.tokens.actual.type == "eof" :
            return a
        else:
            raise ValueError("expressão inválida: Espaço inesperado.")

class PrePro:

    def filter_t(code):
        
        

        

entrada = input("Digite a expressão: ")

saida = Parser.run(entrada)

print('Resultado: {0}'.format(saida))




