import csv
import numpy

with open('input.txt') as file:
    lst = list()
    for line in file.readlines():
        lst.extend(line.rstrip().split(', '))
print(lst)

lst = [float(i) for i in lst]
print(len(lst))
x = numpy.zeros(11, 'f')
f = numpy.zeros(11, 'f')
j = 0
for i in range(len(lst)):
    if i < (len(lst) / 2):
        x[i] = lst[i]
    else:
        f[j] = lst[i]
        j += 1

file2 = open('out1.txt', 'w')
n = 11
m = 7
P = numpy.zeros((11, m))
s = numpy.zeros(m)
file2.write("m = {0}\n".format(m))
file2.write("  X      F")
for i in range(m):
    file2.write("     P{0}".format(i + 1))
file2.write("\n")
for i in range(n):
    file2.write("{0:4.2f}   {1:4.2f}".format(x[i], f[i]))
    for j in range(m):
        file2.write("    {0}".format(P[i][j]))
    file2.write("\n")
file2.write("     S     ")
for i in range(m):
    file2.write("    {0}".format(s[i]))

file2.close()
