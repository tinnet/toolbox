#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import sys

# 1 ≤ m ≤ 1000: the total number of people who entered the lottery.
# 1 ≤ n ≤ m: the total number of winners drawn.
# 1 ≤ t ≤ 100: the number of tickets each winner is allowed to buy.
# 1 ≤ p ≤ m: the number of people in your group.
def parseInput(line):
    return map(int, line.split(" ", 4))

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
    wins_needed = int(math.ceil(float(p)/float(t)))
    if wins_needed > p:
        return 0.0

    # chance is exactly_enough+one_more+two_more...all
    chance = 0.0
    for x in range(wins_needed, p+1):
        # see http://de.wikipedia.org/wiki/Hypergeometrische_Verteilung#Ausf.C3.BChrliches_Rechenbeispiel_f.C3.BCr_die_Kugeln
        chance += (float(binomialCoefficient(p,x)) * float(binomialCoefficient(m - p, n - x))) / float(binomialCoefficient(m,n))
    return chance

def main():
    for line in sys.stdin:
        try:
            m,n,t,p = parseInput(line.strip())
            print "{0:.10f}".format(calculateChance(m,n,t,p))
        except Exception as e:
            print "invalid input line: %s" % line.strip()

    return 0

if __name__ == "__main__":
    sys.exit(main())