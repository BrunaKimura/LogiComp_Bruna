import re

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
            
            elif self.origin[self.position] == '(':
                new_token = Token("(", "(")
                self.actual = new_token
                self.position+=1
            
            elif self.origin[self.position] == ')':
                new_token = Token(")", ")")
                self.actual = new_token
                self.position+=1

            else:
                raise ValueError("token inexistente")
        else:
            new_token = Token("int",int(word))
            self.actual = new_token

        return new_token


class Parser:

    def parserFactor():
        if Parser.tokens.actual.type == 'int':
            resultado = IntVal(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()

        elif Parser.tokens.actual.type == '(':
            Parser.tokens.selectNext()
            resultado = Parser.parserExpression()
            if Parser.tokens.actual.type == ')':
                Parser.tokens.selectNext()
            else:
                raise ValueError("erro: não fechou parênteses")
            

        elif Parser.tokens.actual.type == 'plus':
            Parser.tokens.selectNext()
            children = [Parser.parserFactor()]
            resultado = UnOp('+', children)
            
            
        elif Parser.tokens.actual.type == 'minus':
            Parser.tokens.selectNext()
            children = [Parser.parserFactor()]
            resultado = UnOp('-', children)
            

        else:
            raise ValueError("erro: token inexistente")

        return resultado

    
    def parserTerm():
        resultado = Parser.parserFactor()
        while Parser.tokens.actual.type == 'mult' or Parser.tokens.actual.type == 'div':
            if Parser.tokens.actual.type == 'mult':
                Parser.tokens.selectNext()
                children = [resultado, Parser.parserFactor()]
                resultado = BinOp('*', children)

            if Parser.tokens.actual.type == 'div':
                Parser.tokens.selectNext()
                children = [resultado, Parser.parserFactor()]
                resultado = BinOp('/', children)
            
        return resultado
        

    def parserExpression():
        resultado = Parser.parserTerm()
        while Parser.tokens.actual.type == 'plus' or Parser.tokens.actual.type == 'minus':
            if Parser.tokens.actual.type == 'plus':
                Parser.tokens.selectNext()
                children = [resultado, Parser.parserTerm()]
                resultado = BinOp('+', children)

            if Parser.tokens.actual.type == 'minus':
                Parser.tokens.selectNext()
                children = [resultado, Parser.parserTerm()]
                resultado = BinOp('-', children)
            
        return resultado


    def run(code):
        new_code = PrePro.filter_t(code)
        Parser.tokens = Tokenizer(new_code)
        a = Parser.parserExpression()
        if Parser.tokens.actual.type == "eof" :
            return a
        else:
            raise ValueError("expressão inválida: Espaço inesperado.")

class Node:
    def __init__(self):
        self.value = None
        self.children = []

    def Evaluate(self):
        pass

class BinOp(Node):
    def __init__(self, valor, filho):
        self.value = valor
        self.children = filho

    def Evaluate(self):
        if self.value == '+':
            return self.children[0].Evaluate() + self.children[1].Evaluate()
        elif self.value == '-':
            return self.children[0].Evaluate() - self.children[1].Evaluate()
        elif self.value == '*':
            return self.children[0].Evaluate() * self.children[1].Evaluate()
        elif self.value == '/':
            return self.children[0].Evaluate() // self.children[1].Evaluate()

class UnOp(Node):
    def __init__(self, valor, filho):
        self.value = valor
        self.children = filho

    def Evaluate(self):
        if self.value == '-':
            return -self.children[0].Evaluate()
        else:
            return self.children[0].Evaluate()

class IntVal(Node):
    def __init__(self, valor, filho):
        self.value = valor
        self.children = filho

    def Evaluate(self):
        return self.value

class NoOp(Node):
    def __init__(self, valor, filho):
        self.value = valor
        self.children = filho

    def Evaluate(self):
        pass
                

class PrePro:

    def filter_t(code):
        return re.sub("'.*\n", "" , code, count=0, flags=0)

with open ('entrada.vbs', 'r') as file:
    entrada = file.read() + "\n"

entrada = entrada.replace("\\n","\n")
saida = Parser.run(entrada)

print('Resultado: {0}'.format(saida.Evaluate()))




