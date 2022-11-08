def stairs(n):
    if n == 0:
        return 1
    elif n < 0:
        return 0
    else:
        up_1 = stairs(n-1)
        up_2 = stairs(n-2)
        return up_1 + up_2

print (stairs(3))
