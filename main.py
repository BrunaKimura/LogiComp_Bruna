import re
reserved = ["PRINT", "BEGIN", "END"]
PRINT, BEGIN, END = reserved

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

            elif self.origin[self.position] == '=':
                new_token = Token("assignment", "=")
                self.actual = new_token
                self.position+=1
                
            elif self.origin[self.position] == '\n':
                new_token = Token("lb", "\n")
                self.actual = new_token
                self.position+=1

            elif self.origin[self.position].isalpha():
                word+=self.origin[self.position]
                self.position+=1
                while self.position<len(self.origin) and (self.origin[self.position].isdigit() or self.origin[self.position].isalpha() or self.origin[self.position]=="_"):
                    word+=self.origin[self.position]
                    self.position+=1

                new_word = word.upper()
                
                if word in reserved:
                    new_token = Token(new_word, new_word)
                    self.actual = new_token
                else: 
                    new_token = Token("identifier", new_word)
                    self.actual = new_token


            else:
                raise ValueError("token inexistente")
        else:
            new_token = Token("int",int(word))
            self.actual = new_token

        return new_token


class Parser:

    def parserStatements():
        if Parser.tokens.actual.type == 'BEGIN':
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == 'lb':
                Parser.tokens.selectNext()
                while Parser.tokens.actual.type != 'END'
                    Parser.parserStatement()
                    if Parser.tokens.actual.type != 'lb':
                        raise ValueError("erro: não quebrou a linha")
            else:
                raise ValueError("erro: não quebrou a linha")
        else:
            raise ValueError("erro: não abriu BEGIN")

    def parserStatement():
        if Parser.tokens.actual.type == 'identifier':
            
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == 'assignment':
                Parser.tokens.selectNext()
                Parser.parserExpression()
            else:
                raise ValueError("erro: sem sinal de receber(=)")
        elif Parser.tokens.actual.type == 'PRINT':
            Parser.tokens.selectNext()
            Parser.parserExpression()
        elif Parser.tokens.actual.type == 'BEGIN':
            pass #parseStatement
        elif:
            pass #NoOp
            
            

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
            
        elif Parser.tokens.actual.type == 'identifier':
            ???????????????????????????????????????????????????????????????????????????????????

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


#nós e operadores
class Node:
    def __init__(self):
        self.value = None
        self.children = []

    def Evaluate(self, st)):
        pass

class BinOp(Node):
    def __init__(self, valor, filho):
        self.value = valor
        self.children = filho

    def Evaluate(self, st)):
        if self.value == '+':
            return self.children[0].Evaluate(st) + self.children[1].Evaluate(st)
        elif self.value == '-':
            return self.children[0].Evaluate(st) - self.children[1].Evaluate(st)
        elif self.value == '*':
            return self.children[0].Evaluate(st) * self.children[1].Evaluate(st)
        elif self.value == '/':
            return self.children[0].Evaluate(st) // self.children[1].Evaluate(st)

class UnOp(Node):
    def __init__(self, valor, filho):
        self.value = valor
        self.children = filho

    def Evaluate(self, st)):
        if self.value == '-':
            return -self.children[0].Evaluate(st)
        else:
            return self.children[0].Evaluate(st)

class IntVal(Node):
    def __init__(self, valor, filho):
        self.value = valor
        self.children = filho

    def Evaluate(self, st)):
        return self.value

class NoOp(Node):
    def __init__(self, valor, filho):
        self.value = valor
        self.children = filho

    def Evaluate(self, st)):
        pass


class AssignmentOp(Node):
    def __init__(self, valor, filho):
        self.value = valor
        self.children = filho

    def Evaluate(self, st)):
        return st.setter(self.children[0].value, self.children[1].Evaluate(st))

class PrintOp(Node):
    def __init__(self, valor, filho):
        self.value = valor
        self.children = filho

    def Evaluate(self, st):
        return st.setter(self.children[0].Evaluate(st))

class IdentifierOp(Node):
    def __init__(self, valor, filho):
        self.value = valor
        self.children = filho

    def Evaluate(self, st):
        return st.getter(self.value)

class StatementsOp(Node):
    def __init__(self, valor, filho):
        self.value = valor
        self.children = filho

    def Evaluate(self, st):
        for f in self.children:
            f.Evaluate(st)


#Dicionario de variaveis
class SymbolTable:
    def __init__(self):
        self.dic_variavel = {}

    def getter(self, var):
        if var in self.dic_variavel:
            return self.dic_variavel[var]
        else:
            raise ValueError("erro: variável inexistente")

    def setter(self, var, val):
        self.dic_variavel[var] = val

                

class PrePro:

    def filter_t(code):
        return re.sub("'.*\n", "" , code, count=0, flags=0)


with open ('entrada.vbs', 'r') as file:
    entrada = file.read() + "\n"

entrada = entrada.replace("\\n","\n")
saida = Parser.run(entrada)

st = SymbolTable()

print('Resultado: {0}'.format(saida.Evaluate(st)))