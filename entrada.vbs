Sub main()
    ' adaptado da sabrina

    dim fizz as integer
    dim buzz as integer
    dim fizzbuzz as integer
    dim n as integer
    dim tres as integer
    dim cinco as integer
    dim flag as boolean

    n = 15
    fizz = 30
    buzz = 50
    fizzbuzz = 35
    flag = True

    while n > 0
        print n

        tres = (n - (n / 3 * 3))
        cinco = (n - (n / 5 * 5))
        

        if (tres = 0) and (cinco = 0) then
            print fizzbuzz
            flag = False
        end if

        if (tres = 0) and (flag = True) then
            print fizz
            flag = False
        end if

        if (cinco = 0) and (flag = True) then
            print buzz
            flag = False
        end if

        flag = True
        n = n - 1
    wend
end sub