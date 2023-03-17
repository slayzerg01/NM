import numpy
import matplotlib.pyplot as plt


def Qm(k, x, beta, gamma):
    if k == 0:
        Q = 1
    if k == 1:
        Q = x - beta[0]
    if k > 1:
        Q = (x - beta[k - 1]) * Qm(k - 1, x, beta, gamma) - gamma[k - 2] * Qm(
            k - 2, x, beta, gamma
        )
    return Q


def MNK(x, f, n, m):
    for i in range(11):
        b[0] = b[0] + x[i]
    b[0] = b[0] / 11

    for k in range(1, m, 1):
        znam = 0
        for i in range(n + 1):
            b[k] = b[k] + x[i] * Qm(k, x[i], b, g) * Qm(k, x[i], b, g)
            znam = znam + Qm(k, x[i], b, g) * Qm(k, x[i], b, g)
        b[k] = b[k] / znam

        znam = 0
        for i in range(n + 1):
            g[k - 1] = g[k - 1] + x[i] * Qm(k, x[i], b, g) * Qm(
                k - 1, x[i], b, g
            )
            znam = znam + Qm(k - 1, x[i], b, g) * Qm(k - 1, x[i], b, g)
        g[k - 1] = g[k - 1] / znam

    for k in range(m):
        znam = 0
        for i in range(n + 1):
            a[k] = a[k] + f[i] * Qm(k, x[i], b, g)
            znam = znam + Qm(k, x[i], b, g) * Qm(k, x[i], b, g)
        a[k] = a[k] / znam
    return a, b, g


def Pm(x, alfa, betta, gamma):
    Pm = 0
    for k in range(m):
        Pm = Pm + alfa[k] * Qm(k, x, betta, gamma)
    return Pm


def S(x, f, n, a, b, g):
    d = 0
    for i in range(n):
        d = d + (Pm(x[i], a, b, g) - f[i]) * (Pm(x[i], a, b, g) - f[i])
    return d


def draw(x, f, q, fx):
    plt.plot(x, f, 'o', markersize=5)
    plt.plot(q, fx, linewidth=1)
    plt.xlabel('X', fontsize=12, color='blue')
    plt.ylabel('F(x)', fontsize=12, color='blue')
    plt.title("График полинома", fontsize=16, color='blue')
    plt.grid(True)
    plt.show()

'''
x = [0.0, 0.12, 0.19, 0.35, 0.4, 0.45, 0.62, 0.71, 0.84, 0.91, 1.0]
print(x)
f = [0.8, 1.2, 1.1, 1.7, 1.4, 1.9, 2.4, 3.1, 3.5, 4.1, 3.9]
print(y)
'''

with open('input.txt') as file:
    lst = list()
    for line in file.readlines():
        lst.extend(line.rstrip().split(', '))

lst = [float(i) for i in lst]
x = numpy.zeros(11)
f = numpy.zeros(11)
j = 0
for i in range(len(lst)):
    if i < (len(lst) / 2):
        x[i] = lst[i]
    else:
        f[j] = lst[i]
        j += 1

n = 10
m = 1 + int(input("Введите степень полинома: "))
fx = numpy.zeros(41)
s = numpy.zeros(m)
P = numpy.zeros((11, m))

for i in range(1, m + 1, 1):
    a = numpy.zeros(m)
    b = numpy.zeros(m)
    g = numpy.zeros(m - 1)
    MNK(x, f, n, i)
    s[i - 1] = S(x, f, n, a, b, g)
    for j in range(11):
        P[j][i - 1] = Pm(x[j], a, b, g)

qv = 0
dx = 1 / 40
q = numpy.zeros(41)
for i in range(1, 41, 1):
    qv += dx
    q[i] = qv
for i in range(41):
    fx[i] = Pm(q[i], a, b, g)

outFile = open('out.txt', 'w')
outFile.write("m = {0}\n".format(m - 1))
outFile.write("  X      F")
for i in range(m):
    outFile.write("       P{0}".format(i))
outFile.write("\n")
for i in range(n + 1):
    outFile.write("{0:4.2f}   {1:5.2f}".format(x[i], f[i]))
    for j in range(m):
        outFile.write("    {0:5.2f}".format(P[i][j]))
    outFile.write("\n")
outFile.write("     S     ")
for i in range(m):
    outFile.write("     {0:4.2f}".format(s[i]))
outFile.close()

draw(x, f, q, fx)
