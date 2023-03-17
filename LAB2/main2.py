import numpy
from math import sqrt


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


def Z(n, a, b, eps):
    converge = False
    chek = True
    k = 0
    x = b
    for i in range(n):
        s = 0
        for j in range(n):
            if i != j:
                s += abs(a[i][j] / a[i][i])
        if 1 < s:
            chek = False
    if chek:
        while not converge:
            x_new = numpy.copy(x)
            for i in range(n):
                s1 = sum(a[i][j] * x_new[j] for j in range(i))
                s2 = sum(a[i][j] * x[j] for j in range(i + 1, n))
                x_new[i] = (b[i] - s1 - s2) / a[i][i]

            converge = (
                sqrt(sum((x_new[i] - x[i]) ** 2 for i in range(n))) <= eps
            )
            x = x_new
            k += 1
    else:
        print("метод не сходится")
    return x, k


N = 4
Eps = 1e-06

with open('input.txt') as file:
    lst = list()
    for line in file.readlines():
        lst.extend(line.rstrip().split(', '))
B = numpy.zeros(N)
A = numpy.zeros((N, N))
k = N + 1
for i in range(len(lst)):
    if i < N:
        B[i] = lst[i]
for i in range(N):
    for j in range(N):
        A[i][j] = lst[k]
        k += 1

outFile = open('out.txt', 'w')
outFile.write("N = {0}\n".format(N))
outFile.write("LU метод:\n")
for i in range(N):
    outFile.write("   x{0}       ".format(i + 1))
outFile.write("\n")
for i in range(N):
    outFile.write("{0:8.6f}   ".format((LU(N, A, B, Eps))[i]))
outFile.write("\n\nМетод Зейделя:\n")
outFile.write("Eps = {0}\n".format(Eps))
outFile.write("K = {0}\n".format(Z(N, A, B, Eps)[1]))
for i in range(N):
    outFile.write("   x{0}       ".format(i + 1))
outFile.write("\n")
for i in range(N):
    outFile.write("{0:8.6f}   ".format((Z(N, A, B, Eps))[0][i]))
outFile.close()
