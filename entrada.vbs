Sub Main()
    DIM ba as integer
    Dim i as boolean
    Dim b as boolean
    Dim c as boolean
    i = True
    b = False
    c = i and b
    print not c

    ba = 2
    if ba>3 then
        print ba
    else
        print 4+ba
    end if

    while ba < 10
        print ba
        ba = ba+1
    wend
End Sub