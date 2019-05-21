Sub main()

    dim i as integer
    dim n as integer
    dim f as integer

    n = 5
    i = 2
    f = 1

    while i < n + 1
        f = f * i
        i = i + 1
    wend
    Print f
end sub