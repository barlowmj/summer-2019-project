# function definition for wait_time(tau)

def wait_time(tau):
    if tau == 0:
        return 5*10e-6
    elif tau == 1:
        return 5*30e-6
    elif tau == 2:
        return 5*10e-5
    elif tau == 3:
        return 5*30e-5
    elif tau == 4:
        return 5*10e-4
    elif tau == 5:
        return 5*30e-4
    elif tau == 6:
        return 5*10e-3
    elif tau == 7:
        return 5*30e-3
    elif tau == 8:
        return 5*10e-2
    elif tau == 9:
        return 5*30e-2
    elif tau == 10:
        return 5*10e-1
    elif tau == 11:
        return 5*30e-1
    elif tau == 12:
        return 5*10
    elif tau == 13:
        return 5*30
    elif tau == 14:
        return 5*10e1
    elif tau == 15:
        return 5*30e1
    elif tau == 16:
        return 5*10e2
    elif tau == 17:
        return 5*30e2
    elif tau == 18:
        return 5*10e3
    elif tau == 19:
        return 5*30e3
