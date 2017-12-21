# -*- coding: utf-8 -*-

for x1 in range(1, 9):
    x2 = 9 - x1
    for x3 in range(1, 9):
        if x3 not in (x1, x2):
            x4 = 7 - x3
            if x4 < 1 or x4 > 8 or x4 in (x1, x2, x3):
                continue
            for x5 in range(1, 9):
                if x5 not in (x1, x2, x3, x4):
                    x6 = x5 - 1
                    if x6 < 1 or x6 > 8 or x6 in (x1, x2, x3, x4, x5):
                        continue
                    for x7 in range(1, 9):
                        if x7 not in (x1, x2, x3, x4, x5, x6):
                            x8 = x7 - 2
                            if x8 not in (x1, x2, x3, x4, x5, x6, x7) and x8 > 0 and x8 < 8:
                                print "(%d) + (%d) = 9" % (x1, x2)
                                print "(%d) + (%d) = 7" % (x3, x4)
                                print "(%d) - (%d) = 1" % (x5, x6)
                                print "(%d) - (%d) = 2" % (x7, x8)
                                print "+++++++++++++++++++++++++++"