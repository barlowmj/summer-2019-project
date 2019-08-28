from pylab import plot, show, legend, figure, title, scatter
from numpy import loadtxt, arange
from scipy.optimize import curve_fit

def linear(x, a, b):
    return a*x + b

def main():
    multiplier = arange(4, 4096, 1)

    voltage1 = loadtxt('trial_1.txt', float)
    voltage2 = loadtxt('trial_2.txt', float)
    voltage3 = loadtxt('trial_3.txt', float)
    voltage4 = loadtxt('trial_4.txt', float)

    popt1, pcov1 = curve_fit(linear, multiplier, voltage1)
    popt2, pcov2 = curve_fit(linear, multiplier, voltage2)
    popt3, pcov3 = curve_fit(linear, multiplier, voltage3)
    popt4, pcov4 = curve_fit(linear, multiplier, voltage4)

    popta0 = (popt1[0] + popt2[0] + popt3[0] + popt4[0])/4
    popta1 = (popt1[1] + popt2[1] + popt3[1] + popt4[1])/4

    fit1 = []
    fit2 = []
    fit3 = []
    fit4 = []
    fita = []
    for m in multiplier:
        fit1.append(linear(m, popt1[0], popt1[1]))
        fit2.append(linear(m, popt2[0], popt2[1]))
        fit3.append(linear(m, popt3[0], popt3[1]))
        fit4.append(linear(m, popt4[0], popt4[1]))
        fita.append(linear(m, popta0, popta1))

    res1 = []
    res2 = []
    res3 = []
    res4 = []
    for i in range(len(fit1)):
        res1.append(fit1[i]-voltage1[i])
        res2.append(fit2[i]-voltage2[i])
        res3.append(fit3[i]-voltage3[i])
        res4.append(fit4[i]-voltage4[i])


    figure(1)
    plot(multiplier, fit1)
    scatter(multiplier, voltage1, color = 'r', marker='.')
    legend(['fit', 'raw'])
    title('trial 1')

    figure(2)
    plot(multiplier, fit2)
    scatter(multiplier, voltage2, color = 'r', marker='.')
    legend(['fit', 'raw'])
    title('trial 2')

    figure(3)
    plot(multiplier, fit3)
    scatter(multiplier, voltage3, color = 'r', marker='.')
    legend(['fit', 'raw'])
    title('trial 3')

    figure(4)
    plot(multiplier, fit4)
    scatter(multiplier, voltage4, color = 'r', marker='.')
    legend(['fit', 'raw'])
    title('trial 4')

    figure(5)
    plot(multiplier, fita)
    plot(multiplier, fit1)
    plot(multiplier, fit2)
    plot(multiplier, fit3)
    plot(multiplier, fit4)
    legend(['avg', '1', '2', '3', '4'])
    title('fits and average slope')

    figure(6)
    plot(res1)
    plot(res2)
    plot(res3)
    plot(res4)
    legend(['trial 1', 'trial2', 'trial3', 'trial 4'])
    title('residuals')

    show()

    print(f'The values of popt[0] are {popt1[0]}, {popt2[0]}, {popt3[0]}, and {popt4[0]}.\nTheir average is {popta0}.\nThe '
          f'values of popt[1] are {popt1[1]}, {popt2[1]}, {popt3[1]}, and {popt4[1]}.\nTheir average is {popta1}.')

if __name__ == '__main__':
    main()
