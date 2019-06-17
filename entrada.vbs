Sub check(n as integer)
    dim tres as integer
    dim cinco as integer
    dim flag as boolean
    
    tres = (n - (n / 3 * 3))
    cinco = (n - (n / 5 * 5))
    flag = True

    if (tres = 0) and (cinco = 0) then
        print 53
        flag = False
    end if

    if (tres = 0) and (flag = True) then
        print 3
        flag = False
    end if

    if (cinco = 0) and (flag = True) then
        print 5
    end if
End Sub

Sub fizzBuzz()
    ' adaptado da sabrina
    Dim n as integer

    n = input

    while n > 0
        Call check(n)
        n = n - 1     
    wend
End Sub

Sub main()
    Call fizzBuzz()
end sub