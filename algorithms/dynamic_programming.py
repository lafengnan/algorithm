#! /usr/bin/env python
# coding=utf-8

def _fastest_way(a, t, e, x, n):
    """
    Get the fatest point line 
    L0:    _P0 - P1 --- P2 --- P3 --- P4 ... Pn-1
        e0/   \/  ...                            \_x0
        e1    /\  ...                             _x1 
          \_ /  \                                /
    L1:     P0 - P1 --- P2 --- P3 --- P4 ... Pn-1
    param:
    @a ai,j means the time at a point j on line i
    @t ti,j means the time of moving from point j on line i
    @e ei means the time of entrying line i
    @x xi means the time of leaving line i
    @n means the last point
    """
    f0 = [0] * n
    f1 = [0] * n
    l = [[-1]*n, [-1]*n]
    f_min = l_min = 0

    f0[0] = e[0] + a[0][0]
    f1[0] = e[1] + a[1][0]
    for j in xrange(1, n):
        if f0[j-1] + a[0][j] <= f1[j-1] + t[1][j-1] + a[0][j]:
            f0[j] = f0[j-1] + a[0][j]
            l[0][j] = 0
        else:
            f0[j] = f1[j-1] + t[1][j-1] + a[0][j]
            l[0][j] = 1
        
        if f1[j-1] + a[1][j] <= f0[j-1] + t[0][j-1] + a[1][j]:
            f1[j] = f1[j-1] + a[1][j]
            l[1][j] = 1
        else:
            f1[j] = f0[j-1] + t[0][j-1] + a[1][j]
            l[1][j] = 0

    if f0[n-1] + x[0] <= f1[n-1] + x[1]:
        f_min = f0[n-1] + x[0]
        l_min = 0
    else:
        f_min = f1[n-1] + x[1]
        l_min = 1
    return f_min, l_min, l

def get_stations(a, t, e, x, n, fastest_way_f=_fastest_way):
    min, l_min, l = fastest_way_f(a, t, e, x, n)
    print "fatest value: %d, path is: %d ---> %d" % (min, l_min, n-1)
    i = l_min
    for j in xrange(n-1, 0, -1):
        i = l[i][j]
        print "line %d, station %d" % (i, j - 1)


def _lcs_length(x, y):
    m = len(x)
    n = len(y)
    c = [[0 for _ in xrange(0, n+1)] for _ in xrange(0, m+1)]
    b = [[0 for _ in xrange(0, n+1)] for _ in xrange(0, m+1)]
    for i in xrange(1, m+1):
        c[i][0] = 0

    for j in xrange(0, n+1):
        c[0][j] = 0

    for i in xrange(1, m+1):
        for j in xrange(1, n+1):
            if x[i-1] == y[j-1]:
                c[i][j] = c[i-1][j-1] + 1
                b[i][j] = "*"
            elif c[i-1][j] >= c[i][j-1]:
                c[i][j] = c[i-1][j]
                b[i][j] = "^"
            else:
                c[i][j] = c[i][j-1]
                b[i][j] = "<"

    return c, b

def get_lcs(x, b, len_x, len_y, lcs=[]):
    m = len_x
    n = len_y
    if m == 0 or n == 0:
        return
    if b[m][n] == "*":
        get_lcs(x, b, m-1, n-1, lcs)
        lcs.append(x[m-1])
    elif b[m][n] == "^":
        get_lcs(x, b, m-1, n, lcs)
    else:
        get_lcs(x, b, m, n-1, lcs)

if __name__ == '__main__':
    a = [[7, 9, 3, 4, 8, 4], [8, 5, 6, 4, 5, 7]]
    e = [2, 4]
    x = [3, 2]
    t = [[2, 3, 1, 3, 4, 0], [2, 1, 2, 2, 1, 0]]
    get_stations(a, t, e, x, 6)

    x = "ABCBDAB"
    y = "BDCABA"
    b = _lcs_length(x, y)[1]
    lcs = []
    get_lcs(x, b, len(x), len(y), lcs)
    print lcs
