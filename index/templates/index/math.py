for a in range(0,100):
    for b in range(0,100):
        for c in range(0,100):
            if (a+b-c)!=0 and (a+c-b)!=0:
                if (a+b+c)/(a+b-c)==3 and (a+b+c)/(a+c-b)==2.25 and (a+b-c)!=0 and (a+c-b)!=0:
                    print(a,b,c) 