#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import sys

# 1 ≤ m ≤ 1000: the total number of people who entered the lottery.
# 1 ≤ n ≤ m: the total number of winners drawn.
# 1 ≤ t ≤ 100: the number of tickets each winner is allowed to buy.
# 1 ≤ p ≤ m: the number of people in your group.
def parseInput(line):
    return map(float, line.split(" ", 4))

# from http://en.wikipedia.org/wiki/Binomial_coefficient#Binomial_coefficient_in_programming_languages
def binomialCoefficient(n, k):
    if k < 0 or k > n:
        return 0
    if k > n - k: # take advantage of symmetry
        k = n - k
    c = 1
    for i in range(k):
        c *= n - (k - (i+1))
        c //= i+1
    return c


def calculateChance(m,n,t,p):
    wins_needed = math.ceil(p/t)
    chance_to_win = (n/m)*p
    print wins_needed, chance_to_win
    print binomialCoefficient(20,4)
    return chance_to_win**wins_needed

def main():
    for line in sys.stdin:
        try:
            m,n,t,p = parseInput(line.strip())
            print "{0:.10f}".format(calculateChance(m,n,t,p))
        except Exception:
            print "invalid input line: %s" % line.strip()

    return 0

if __name__ == "__main__":
    sys.exit(main())