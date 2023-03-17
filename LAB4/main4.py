import numpy
import math


def fct(t, Y, F):
    F[0] = Y[1]
    F[1] = 500 * t + 126 - 504 * Y[1] - 2000 * Y[0]


def rk4(n, Y, h, t):
    k1 = numpy.zeros(n)
    k2 = numpy.zeros(n)
    k3 = numpy.zeros(n)
    k4 = numpy.zeros(n)
    Fk = numpy.zeros(n)
    Yk1 = numpy.zeros(n)
    fct(t, Y, Fk)
    for i in range(n):
        k1[i] = h * Fk[i]
    for i in range(n):
        Yk1[i] = Y[i] + k1[i] / 2
    fct(t + h / 2, Yk1, Fk)
    for i in range(n):
        k2[i] = h * Fk[i]
    for i in range(n):
        Yk1[i] = Y[i] + k2[i] / 2
    fct(t + h / 2, Yk1, Fk)
    for i in range(n):
        k3[i] = h * Fk[i]
    for i in range(n):
        Yk1[i] = Y[i] + k3[i]
    fct(t + h, Yk1, Fk)
    for i in range(n):
        k4[i] = h * Fk[i]

    for i in range(n):
        Y[i] += (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6


def adm(t, F0, F1, F2, F3, Y):
    Yk = numpy.zeros(n)
    Fk = numpy.zeros(n)
    for i in range(n):
        Yk[i] = (
            Y[i] + h * (55 * F3[i] - 59 * F2[i] + 37 * F1[i] - 9 * F0[i]) / 24
        )
    fct(t, Yk, Fk)
    for i in range(n):
        Y[i] += h * (9 * Fk[i] + 19 * F3[i] - 5 * F2[i] + F1[i]) / 24
    fct(t, Y, Fk)
    for i in range(n):
        F0[i] = F1[i]
        F1[i] = F2[i]
        F2[i] = F3[i]
        F3[i] = Fk[i]


def out(Y, Yk, t, k):
    adblock = False
    rublock = False
    Yan = numpy.zeros(n)
    Yan[0] = 2 * math.exp(-4 * t) + t / 4
    Yan[1] = -8 * math.exp(-4 * t) + 1 / 4
    if k % 25 == 0 or k <= 4:
        if abs(Yan[0] - Y[0]) > 1 or abs(Yan[1] - Y[1]) > 1:
            rublock = True
        if abs(Yan[0] - Yk[0]) > 1 or abs(Yan[1] - Yk[1]) > 1:
            adblock = True
        if rublock:
            outFile.write(
                "{:0<5.3} {:>13}  {:>13}  {:0<13.9}  {:>13}  {:>13}  {:0<13.9}\n".format(
                    int(t * 1000) / 1000,
                    str("none"),
                    str("none"),
                    Yan[0],
                    str("none"),
                    str("none"),
                    Yan[1],
                )
            )
        elif adblock:
            outFile.write(
                "{:0<5.3} {:0<13.9}  {:>13}  {:0<13.9}  {:0<13.9}  {:>13}  {:0<13.9}\n".format(
                    int(t * 1000) / 1000,
                    Y[0],
                    str("none"),
                    Yan[0],
                    Y[1],
                    str("none"),
                    Yan[1],
                )
            )

        else:
            outFile.write(
                "{:0<5.3} {:0<13.9}  {:0<13.9}  {:0<13.9}  {:0<13.9}  {:0<13.9}  {:0<13.9}\n".format(
                    int(t * 1000) / 1000,
                    Y[0],
                    Yk[0],
                    Yan[0],
                    Y[1],
                    Yk[1],
                    Yan[1],
                )
            )


n = 2
t0 = 0
tk = 3
h = 0.0056
Y = numpy.zeros(2)
Y[0] = 2
Y[1] = -7.75
t = t0
outFile = open('out.txt', 'w')
outFile.write(
    "  t    Yрунге-кутта     Yадамса    Yаналитический  Y'рунге-кутта    Y'адамса    Y'аналитический\n"
)
Y1 = list(Y)
out(Y, Y1, t, 0)
t = t0 + h
rk4(n, Y, h, t)
Y2 = list(Y)
out(Y, Y2, t, 1)
t = t0 + 2 * h
rk4(n, Y, h, t)
Y3 = list(Y)
out(Y, Y3, t, 2)
t = t0 + 3 * h
rk4(n, Y, h, t)
Y4 = list(Y)
out(Y, Y4, t, 3)
Yk = list(Y)
k = 4
while t <= tk:
    t = t0 + h * k
    rk4(n, Y, h, t)
    adm(t, Y1, Y2, Y3, Y4, Yk)
    out(Y, Yk, t, k)
    k += 1
outFile.close()
