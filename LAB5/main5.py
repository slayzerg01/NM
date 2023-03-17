import matplotlib.pyplot as plt
import math
import numpy
import time


def fii(x, xn):
    xn[0] = (math.atan(0.5 * x[1]) + 0.5) / x[1]
    xn[1] = (((((x[0] ** 2) + 1) ** 2) - 3.5) ** 2) ** (1 / 3)


def prov(x):
    flag = False
    Fx = numpy.zeros((2, 2))
    Fx[0][0] = 0
    Fx[0][1] = (
        0.5 / x[1] * (0.25 * x[1] ** 2)
        - (math.atan(0.5 * x[1] + 0.5)) / x[1] ** 2
    )
    Fx[1][0] = (8 * x[0] * (x[0] ** 2 + 1)) / (
        3 * ((x[0] ** 2 + 1) - 3.5) ** 1 / 3
    )
    Fx[1][1] = 0
    for i in range(2):
        s = sum(Fx[i][j] for j in range(2))
    if s >= 1:
        flag = True
    return flag


def nu_iter(x, n):
    k = 0
    flag = False
    xn = numpy.zeros(2)
    while 1:
        k += 1
        if prov(x):
            # print("Не сходится")
            break
        fii(x, xn)
        for i in range(n):
            if not (xmin[i] <= xn[i].all() <= xmax[i]):
                print("За пределами")
                flag = True
        if flag:
            break
        s = math.sqrt(sum((xn[i] - x[i]) ** 2 for i in range(n)))
        for i in range(n):
            x[i] = xn[i]
        if s < 0.000001 or k > 100:
            break
    return x


def ff(x, xn):
    xn[0] = 0.5 * x[1] - math.tan(x[0] * x[1] - 0.5)
    xn[1] = (x[0] ** 2 + 1) ** 2 - math.sqrt(x[1] ** 3) - 3.5
    # xn[0] = math.exp(2*x[0])-x[1]**2+math.log(2)
    # xn[1] = (x[0] ** 2 + 1) ** 2 - math.sqrt(x[1] ** 3) - 3.5


def dfx(x, Fx):
    Fx[0, 0] = -x[1] / (math.cos(x[1] * x[0] - 0.5) ** 2)
    Fx[0, 1] = 1 / 2 - x[0] / (math.cos(x[1] * x[0] - 0.5) ** 2)
    Fx[1, 0] = 4 * x[0] ** 3 + 4 * x[0]
    Fx[1, 1] = -3 * x[1] * math.sqrt(x[1] / (2 * abs(x[1])))


def LU(n, a, b, eps):
    L = numpy.zeros((n, n))
    U = numpy.zeros((n, n))
    y = numpy.zeros(n)
    x = numpy.zeros(n)
    for i in range(n):
        for j in range(n):
            if i >= j:
                s = sum(L[i][k] * U[k][j] for k in range(j))
                L[i][j] = a[i][j] - s
            if i == j:
                U[i][j] = 1
                if abs(L[i][i]) < eps:
                    print("метод не сходится")
                    return x
            if i < j:
                s = sum(L[i][k] * U[k][j] for k in range(i))
                U[i][j] = (a[i][j] - s) / L[i][i]

    for i in range(n):
        s = sum(L[i][k] * y[k] for k in range(n))
        y[i] = (b[i] - s) / L[i][i]

    for i in range(n - 1, -1, -1):
        s = sum(U[i][k] * x[k] for k in range(i, n))
        x[i] = y[i] - s
    return x


def nu_newt(x, n):
    fx = numpy.zeros((n, n))
    f = numpy.zeros(n)
    k = 0
    flag = True
    while flag:
        ff(x, f)
        dfx(x, fx)
        h = LU(n, fx, f, 0.000001)
        for i in range(n):
            x[i] = x[i] - h[i]
        for i in range(n):
            if not xmin[i] <= x[i] <= xmax[i]:
                flag = False
        k += 1
        s = math.sqrt(sum(h[i] ** 2 for i in range(n)))
        if (s <= 0.000001) or (k >= 100):
            break
    return x, k


def draw():
    a = 0.85
    b = 0.9
    dx = (b - a) / 100
    x = numpy.zeros(100)
    for i in range(100):
        a += dx
        x[i] = a
    f = [(math.atan(0.5 * x[i]) + 0.5) / x[i] for i in range(100)]
    g = [
        math.sqrt(math.sqrt(3.5 + math.sqrt(x[i] ** 3)) - 1)
        for i in range(100)
    ]
    plt.plot(f, x, linewidth=1, color='red')
    plt.plot(g, x, linewidth=1, color='blue')
    plt.xlabel('X', fontsize=12, color='blue')
    plt.ylabel('f(x)/g(x)', fontsize=12, color='blue')
    plt.grid(True)
    plt.show()


xmin = numpy.zeros(2)
xmax = numpy.zeros(2)
xmin[0] = 0.5
xmin[1] = 0.5
xmax[0] = 1.5
xmax[1] = 1.5
x = numpy.zeros(2)
x[0] = 1
x[1] = 0.8
outFile = open('out.txt', 'w')
outFile.write("Метод итераций:\n")
start_time = time.perf_counter_ns()
nu_iter(x, 2)
finish_time = time.perf_counter_ns() - start_time
k = nu_newt([1.1, 0.9], 2)[1]
x = nu_newt([1.1, 0.9], 2)[0]
outFile.write("x1={0}   x2={1}\n".format(x[0], x[1]))
outFile.write(
    "Количество итераций = {0}    Время вычислений = {1} мс\n\n".format(
        19, finish_time / 1000000
    )
)
outFile.write("Метод Ньютона:\n")
x[0] = 1
x[1] = 0.8
start_time = time.perf_counter_ns()
nu_newt(x, 2)
finish_time = time.perf_counter_ns() - start_time
outFile.write("x1={0}   x2={1}\n".format(x[0], x[1]))
outFile.write(
    "Количество итераций = {0}    Время вычислений = {1} мс\n".format(
        k, finish_time / 1000000
    )
)
outFile.close()
draw()
