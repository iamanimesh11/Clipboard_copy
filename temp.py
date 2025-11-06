def rev(Str):
    if len(Str)<0:
        return "" 
    print(Str)
    return Str[len(Str)-1]+rev(Str[::-1])

rev("animesh")
