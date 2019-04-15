import re
import sys

reserved = ["PRINT", "END", "OR", "AND", "INPUT", "WHILE", "IF", "THEN", "WEND", "ELSE", "NOT", "MAIN", "SUB", "DIM", "AS", "INTERGER", "BOOLEAN"]
PRINT, END, OR, AND, INPUT, WHILE, IF, THEN, WEND, ELSE, NOT, MAIN, SUB, DIM, AS, INTERGER, BOOLEAN = reserved

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

        while self.position<len(self.origin) and self.origin[self.position].isspace() and self.origin[self.position]!="\n":
            self.position+=1

        if self.position == len(self.origin):
            new_token = Token("eof", "")
            word = 'eof'
            self.actual = new_token

            return new_token

        if self.origin[self.position] == '\n':
            new_token = Token("lb", "\n")
            self.actual = new_token
            self.position+=1
            return new_token

        while self.position<len(self.origin) and self.origin[self.position].isdigit():
            word+=self.origin[self.position]
            self.position+=1

        if word == "":
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

            elif self.origin[self.position] == '>':
                new_token = Token(">", ">")
                self.actual = new_token
                self.position+=1

            elif self.origin[self.position] == '<':
                new_token = Token("<", "<")
                self.actual = new_token
                self.position+=1

            elif self.origin[self.position].isalpha():
                word+=self.origin[self.position]
                self.position+=1
                while self.position<len(self.origin) and (self.origin[self.position].isdigit() or self.origin[self.position].isalpha() or self.origin[self.position]=="_"):
                    word+=self.origin[self.position]
                    self.position+=1

                new_word = word.upper()
                
                if new_word in reserved:
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

    def parserProgram():
        if Parser.tokens.actual.type == 'SUB':
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == 'MAIN':
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == '(':
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == ')':
                        Parser.tokens.selectNext()
                        if Parser.tokens.actual.type == 'lb':
                            Parser.tokens.selectNext()

                            lista_resultado = []
                            while Parser.tokens.actual.type != 'END':
                                lista_resultado.append(Parser.parserStatement())
                                if Parser.tokens.actual.type == 'lb':
                                Parser.tokens.selectNext()

                            Parser.tokens.selectNext()

                            if Parser.tokens.actual.type == 'sub':
                                Parser.tokens.selectNext()
                                return StatementsOp("statement", lista_resultado)
                            
                            else:
                                raise ValueError("erro program: não fechou sub")

                        else:
                            raise ValueError("erro program: não pilou linha")
            
                    else:
                        raise ValueError("erro program: não fechou parênteses")
        
                else:
                    raise ValueError("erro program: não abriu parênteses")
    
            else:
                raise ValueError("erro program: não abriu main")
        else:
            raise ValueError("erro program: não abriu sub")
              

    def parserStatement():
        if Parser.tokens.actual.type == 'identifier':
            variavel = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == 'assignment':
                sinal = Parser.tokens.actual.value 
                Parser.tokens.selectNext()
                resultado = AssignmentOp(sinal, [variavel, Parser.parserRelExpression()])    
            else:
                raise ValueError("erro: sem sinal de receber(=)")
        elif Parser.tokens.actual.type == 'PRINT':
            Parser.tokens.selectNext()
            resultado = PrintOp("PRINT", [Parser.parserRelExpression()])

        elif Parser.tokens.actual.type == 'WHILE':
            Parser.tokens.selectNext()
            filhos = [Parser.parserRelExpression()]

            if Parser.tokens.actual.type == 'lb':
                Parser.tokens.selectNext()

                while Parser.tokens.actual.type != 'WEND':
                    filhos.append(Parser.parserStatement())
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == 'lb':
                        Parser.tokens.selectNext()
                    else:
                        raise ValueError("erro: não pulou linha")

            else:
                raise ValueError("erro: não pulou linha")

            if Parser.tokens.actual.type == 'WEND':
                Parser.tokens.selectNext()
                resultado = WhileOp("while", filhos)
            else:
                raise ValueError("erro: não fechou o while")

        elif Parser.tokens.actual.type == 'IF':
            lista_filhos = []
            Parser.tokens.selectNext()
            lista_filhos.append(Parser.parserRelExpression())
            if Parser.tokens.actual.type == 'THEN':
                Parser.tokens.selectNext()
                lista_if = []
                while Parser.tokens.actual.type != 'ELSE' or Parser.tokens.actual.type != 'END':
                    lista_if.append(Parser.parserStatement())
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == 'lb':
                        Parser.tokens.selectNext()
                    else:
                        raise ValueError("erro: não pulou linha")

                lista_filhos.append(lista_if)

                if Parser.tokens.actual.type == 'ELSE':
                    Parser.tokens.selectNext()
                    lista_else = []
                    while Parser.tokens.actual.type != 'END':
                        lista_else.append(Parser.parserStatement())
                        Parser.tokens.selectNext()
                        if Parser.tokens.actual.type == 'lb':
                            Parser.tokens.selectNext()
                        else:
                            raise ValueError("erro: não pulou linha")
                
                lista_filhos.append(lista_else)

                if Parser.tokens.actual.type == 'END':
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == 'IF':
                        Parser.tokens.selectNext()
                        resultado = IfOp("IF", lista_filhos)
                    else:
                        raise ValueError("erro: não fechou o if")
                else:
                    raise ValueError("erro: não fechou o end do if")

            else:
                raise ValueError("erro: esqueceu o 'then'")

            

        else:
            resultado = NoOp(0, [])

        return resultado

    def parserRelExpression():
        valor1 = Parser.parserExpression()
        if Parser.tokens.actual.type == "assignment":
            Parser.tokens.selectNext()
            valor2 = Parser.parserExpression()
            resultado = BinOp("=", [valor1, valor2])

        elif Parser.tokens.actual.type == ">":
            Parser.tokens.selectNext()
            valor2 = Parser.parserExpression()
            resultado = BinOp(">", [valor1, valor2])

        elif Parser.tokens.actual.type == "<":
            Parser.tokens.selectNext()
            valor2 = Parser.parserExpression()
            resultado = BinOp("<", [valor1, valor2])

        else:
            raise ValueError("erro: expressão não identificada")

        return resultado

    def parserExpression():
        resultado = Parser.parserTerm()
        while Parser.tokens.actual.type == 'plus' or Parser.tokens.actual.type == 'minus' or Parser.tokens.actual.type == 'OR':
            if Parser.tokens.actual.type == 'plus':
                Parser.tokens.selectNext()
                children = [resultado, Parser.parserTerm()]
                resultado = BinOp('+', children)

            if Parser.tokens.actual.type == 'minus':
                Parser.tokens.selectNext()
                children = [resultado, Parser.parserTerm()]
                resultado = BinOp('-', children)

            if Parser.tokens.actual.type == 'OR':
                Parser.tokens.selectNext()
                children = [resultado, Parser.parserTerm()]
                resultado = BinOp('or', children)
            
        return resultado


    def parserTerm():
        resultado = Parser.parserFactor()
        while Parser.tokens.actual.type == 'mult' or Parser.tokens.actual.type == 'div' or Parser.tokens.actual.type == 'AND':
            if Parser.tokens.actual.type == 'mult':
                Parser.tokens.selectNext()
                children = [resultado, Parser.parserFactor()]
                resultado = BinOp('*', children)

            if Parser.tokens.actual.type == 'div':
                Parser.tokens.selectNext()
                children = [resultado, Parser.parserFactor()]
                resultado = BinOp('/', children)

            if Parser.tokens.actual.type == 'AND':
                Parser.tokens.selectNext()
                children = [resultado, Parser.parserFactor()]
                resultado = BinOp('and', children)
            
        return resultado


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

        elif Parser.tokens.actual.type == 'NOT':
            Parser.tokens.selectNext()
            children = [Parser.parserFactor()]
            resultado = UnOp('not', children)
            
        elif Parser.tokens.actual.type == 'identifier':
            resultado = IdentifierOp(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()

        elif Parser.tokens.actual.type == 'INPUT':
            resultado = InputOp('',[])
            Parser.tokens.selectNext()

        else:
            raise ValueError("erro: token inexistente")

        return resultado


    def run(code):
        new_code = PrePro.filter_t(code)
        Parser.tokens = Tokenizer(new_code)
        a = Parser.parserStatements()
        Parser.tokens.selectNext()
        while Parser.tokens.actual.type == 'lb':
            Parser.tokens.selectNext()
        if Parser.tokens.actual.type == "eof":
            return a
        else:
            raise ValueError("erro: eof não encontrado")


#nós e operadores
class Node:
    def __init__(self):
        self.value = None
        self.children = []

    def Evaluate(self, st):
        pass

class BinOp(Node):
    def __init__(self, valor, filho):
        self.value = valor
        self.children = filho

    def Evaluate(self, st):
        if self.value == '+':
            return self.children[0].Evaluate(st) + self.children[1].Evaluate(st)
        elif self.value == '-':
            return self.children[0].Evaluate(st) - self.children[1].Evaluate(st)
        elif self.value == '*':
            return self.children[0].Evaluate(st) * self.children[1].Evaluate(st)
        elif self.value == '/':
            return self.children[0].Evaluate(st) // self.children[1].Evaluate(st)
        elif self.value == '=':
            return self.children[0].Evaluate(st) == self.children[1].Evaluate(st)
        elif self.value == '>':
            return self.children[0].Evaluate(st) > self.children[1].Evaluate(st)
        elif self.value == '<':
            return self.children[0].Evaluate(st) < self.children[1].Evaluate(st)
        elif self.value == 'OR':
            return self.children[0].Evaluate(st) or self.children[1].Evaluate(st)
        elif self.value == 'AND':
            return self.children[0].Evaluate(st) and self.children[1].Evaluate(st)

class UnOp(Node):
    def __init__(self, valor, filho):
        self.value = valor
        self.children = filho

    def Evaluate(self, st):
        if self.value == '-':
            return -self.children[0].Evaluate(st)
        elif self.value == '+':
            return self.children[0].Evaluate(st)
        else:
            return not(self.children[0].Evaluate(st))

class IntVal(Node):
    def __init__(self, valor, filho):
        self.value = valor
        self.children = filho

    def Evaluate(self, st):
        return self.value

class NoOp(Node):
    def __init__(self, valor, filho):
        self.value = valor
        self.children = filho

    def Evaluate(self, st):
        pass


class AssignmentOp(Node):
    def __init__(self, valor, filho):
        self.value = valor
        self.children = filho

    def Evaluate(self, st):
        return st.setter(self.children[0], self.children[1].Evaluate(st))

class PrintOp(Node):
    def __init__(self, valor, filho):
        self.value = valor
        self.children = filho

    def Evaluate(self, st):
        print(self.children[0].Evaluate(st))

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

class WhileOp(Node):
    def __init__(self, valor, filho):
        self.value = valor
        self.children = filho

    def Evaluate(self, st):
        while self.children[0].Evaluate(st):
            self.children[1].Evaluate(st)

class InputOp(Node):
    def __init__(self, valor, filho):
        self.value = valor
        self.children = filho

    def Evaluate(self, st):
        return int(input(""))

class IfOp(Node):
    def __init__(self, valor, filho):
        self.value = valor
        self.children = filho

    def Evaluate(self, st):
        if self.children[0].Evaluate(st):
            return self.children[1].Evaluate(st)
        else:
            if len(self.children) == 3:
                return self.children[2].Evaluate(st)
            else:
                pass


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

st = SymbolTable()

if len(sys.argv) == 1:
    raise ValueError("erro: arquivo de entrada não inserido ")
script = sys.argv[0]
filename = sys.argv[1]

# filename = 'entrada.vbs'

with open (filename, 'r') as file:
    entrada = file.read() + "\n"

entrada = entrada.replace("\\n","\n")
saida = Parser.run(entrada)
saida.Evaluate(st)