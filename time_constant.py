# function definition for time_const(f)

def time_const(f):
    if f > 5e5:
        return 0
    elif f > (1e6)/6:
        return 1
    elif f > 5e4:
        return 2
    elif f > (1e5)/6:
        return 3
    elif f > 5e3:
        return 4
    elif f > (1e4)/6:
        return 5
    elif f > 5e2:
        return 6
    elif f > (1e3)/6:
        return 7
    elif f > 5e1:
        return 8
    elif f > (1e2)/6:
        return 9
    elif f > 5:
        return 10
    elif f > (1e1)/6:
        return 11
    elif f > 5e-1:
        return 12
    elif f > 1/6:
        return 13
    elif f > 5e-2:
        return 14
    elif f > (1e-1)/6:
        return 15
    elif f > 5e-3:
        return 16
    elif f > (1e-2)/6:
        return 17
    elif f > 5e-4:
        return 18
    elif f > (1e-3)/6:
        return 19
