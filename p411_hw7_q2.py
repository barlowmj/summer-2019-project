# Problem 2: Fourier filtering and smoothing

from numpy import loadtxt
from pylab import plot, show, figure, title, suptitle, legend
from numpy.fft import rfft, irfft
from dcst import dct, idct

# (a) Read in data from dow.txt and plot it

dow = loadtxt('dow.txt')

figure(1)
plot(dow)
title('DOW daily closing value, late 2006 - end 2010')
suptitle('Problem 2(a)')

# (b) calculate the Fourier coefficients of the data using rfft, array of 0.5*N + 1 values

c_dow = rfft(dow)

# (c) set all but the first 10% of values to 0

N = len(dow)
ten_percent = int(0.1*(0.5*N+1))
c_dow[ten_percent:-1] = 0

# (d) calculate the inverse Fourier transform, and plot it on the same graph as the original, comment on what you see

dow_new = irfft(c_dow)

figure(2)
plot(dow, color='r')
plot(dow_new, color='b')
legend(['Original', '10%'])
title('DOW closing value, late 2006 - end 2010 with Fourier smoothing')
suptitle('Problem 2(d)')

# this operation smooths the function

# (e) set all but the first 2% of coefficients to zero, and plot all three on the same plot

two_percent = int(0.02*(0.5*N+1))
c_dow[two_percent:-1] = 0
dow_new_2 = irfft(c_dow)

figure(3)
plot(dow, color='r')
plot(dow_new, color='b')
plot(dow_new_2, color='g')
legend(['Original', '10%', '2%'])
title('DOW closing value, late 2006 - end 2010 with (more) Fourier smoothing')
suptitle('Problem 2(e)')

# (f) read in dow2.txt, plotting all the values and the 2%

dow2 = loadtxt('dow2.txt')

c_dow2 = rfft(dow2)
N = len(dow2)
two_percent = int(0.02*(0.5*N+1))
c_dow2[two_percent:-1] = 0
dow2_new = irfft(c_dow2)

figure(4)
plot(dow2, color='r')
plot(dow2_new, color='b')
legend(['Original', '2%'])
title('DOW closing value, 2004 - 2008 with Fourier smoothing using FFT')
suptitle('Problem 2(f)')

# (g) modify to perform discrete cosine transform

cosine_c_dow2 = dct(dow2)
cosine_c_dow2[two_percent:-1] = 0
dow2_new_cosine = idct(cosine_c_dow2)

figure(5)
plot(dow2, color='r')
plot(dow2_new_cosine, color='b')
legend(['Original', '2%'])
title('DOW closing value, 2004 - 2008 with Fourier smoothing using DCT')
suptitle('Problem 2(g)')

show()

# from parts (f) and (g), we can see that the dct function applies to non-periodic functions as well, and fft is strictly suited to periodic functions, causing huge distortion when used on non-periodic data sets.
