import numpy
import math


def iter(a1, n, e):
    z = [1] * n
    y1 = numpy.zeros(n)
    l1 = numpy.zeros(30)
    v = numpy.zeros(n)
    y2 = numpy.zeros(n)
    l2 = numpy.zeros(200)
    eps = True
    k1 = 0
    while eps:
        for i in range(n):
            y1[i] = sum(a1[i][j] * z[j] for j in range(n))

        l1[k1] = sum(y1[i] * z[i] for i in range(n))

        for i in range(n):
            z[i] = y1[i] / math.sqrt(sum(y1[i] * y1[i] for i in range(n)))

        Eps = math.sqrt(
            sum(
                (y1[i] - l1[k1] * z[i]) * (y1[i] - l1[k1] * z[i])
                for i in range(n)
            )
        )
        if Eps < e:
            L1 = l1[k1]
            x1 = z
            eps = False
        k1 += 1

    z = [1] * n
    eps2 = True
    k2 = 0
    while eps2:
        for i in range(n):
            v[i] = sum(a1[i][j] * z[j] for j in range(n))

        l2[k2] = sum(v[i] * z[i] for i in range(n))
        p = sum(v[i] * x1[i] for i in range(n))
        for i in range(n):
            y2[i] = v[i] - p * x1[i]

        for i in range(n):
            z[i] = y2[i] / math.sqrt(sum(y2[i] * y2[i] for i in range(n)))

        Eps = math.sqrt(
            sum(
                (y2[i] - l2[k2] * z[i]) * (y2[i] - l2[k2] * z[i])
                for i in range(n)
            )
        )
        if Eps < e:
            L2 = l2[k2]
            x2 = z
            eps2 = False
        k2 += 1
    return L1, L2, x1, x2, k1, k2


def vrash(a, n, e):
    global k3
    k3 = 0
    v = numpy.zeros((n, n))
    h = numpy.zeros((n, n))
    hh = numpy.zeros((n, n))
    s1 = numpy.zeros((n, n))
    s2 = numpy.zeros((n, n))
    chek = True
    while chek:
        imax = 0
        jmax = 1
        max = a[0][1]
        for i in range(n):
            for j in range(n):
                if i < j:
                    if abs(max) < abs(a[i][j]):
                        max = a[i][j]
                        imax = i
                        jmax = j
        if a[imax][imax] == a[jmax][jmax]:
            f = math.pi / 4
        else:
            f = 0.5 * (
                math.atan(2 * a[imax][jmax] / (a[imax][imax] - a[jmax][jmax]))
            )

        for i in range(n):
            for j in range(n):
                if i != j:
                    h[i, j] = 0
                else:
                    h[i, j] = 1
        h[imax][imax] = math.cos(f)
        h[jmax][jmax] = math.cos(f)
        h[imax][jmax] = -math.sin(f)
        h[jmax][imax] = math.sin(f)

        if k3 == 0:
            for i in range(n):
                for j in range(n):
                    v[i][j] = h[i][j]
        else:
            for i in range(n):
                for l in range(n):
                    s1[i][l] = sum(v[i][j] * h[j][l] for j in range(n))
            for i in range(n):
                for j in range(n):
                    v[i][j] = s1[i][j]

        for i in range(n):
            for j in range(n):
                hh[i][j] = h[j][i]

        for i in range(n):
            for l in range(n):
                s2[i][l] = sum(hh[i, j] * a[j][l] for j in range(n))

        for i in range(n):
            for l in range(n):
                a[i][l] = sum(s2[i][j] * h[j][l] for j in range(n))

        if abs(max) < e:
            chek = False
        k3 += 1

    for i in range(n):
        v[i][n - 1] = v[i][n - 1] / math.sqrt(
            sum(v[j][n - 1] * v[j][n - 1] for j in range(n))
        )
    return v, a, k3


N = 5
E = 0.000001

with open('input.txt') as file:
    lst = list()
    for line in file.readlines():
        lst.extend(line.rstrip().split(', '))
a = numpy.zeros((N, N))
k = 0
for i in range(N):
    for j in range(N):
        a[i][j] = lst[k]
        k += 1

outFile = open('out.txt', 'w')
outFile.write("Метод итераций:\n")
outFile.write(
    "Собственное значение L1 = {0}      Число итераций = {1}  \n".format(
        iter(a, N, E)[1], iter(a, N, E)[5]
    )
)
outFile.write("Собственный вектор x1:\n")
for i in range(N):
    outFile.write(" {:>13.10}  ".format(iter(a, N, E)[3][i]))
outFile.write(
    "\nСобственное значение L2 = {0}      Число итераций = {1}\n".format(
        iter(a, N, E)[0], iter(a, N, E)[4]
    )
)
outFile.write("Собственный вектор x2:\n")
for i in range(N):
    outFile.write(" {:>13.10}  ".format(iter(a, N, E)[2][i]))

outFile.write("\n\nМетод вращений:\n")
V = vrash(a, N, E)[0]
outFile.write("Число итераций = {0} \n".format(k3))
for i in range(N):
    outFile.write("Собственное значение L{0} = {1}\n".format(i + 1, a[i][i]))
    outFile.write("Собственный вектор x{0}:\n".format(i + 1))
    for j in range(N):
        outFile.write(" {:>13.10}   ".format(V[j][i]))
    outFile.write("\n")
outFile.close()
