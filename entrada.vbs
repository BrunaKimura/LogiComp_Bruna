Function Soma(x as Integer, y as Integer) as Integer
    Dim a as Integer
    a=x+y
    print a
    while a < 10
        a=Soma(a, 1)
    wend
    
    Soma = a
 
End Function


Sub main()
    Dim a as Integer
    Dim b as Integer
    a=3
    b=Soma(a,4)
    print a
    print b
end sub