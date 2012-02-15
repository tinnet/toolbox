#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

FRIEND = 1009

def parseInput():
    team_count = int(sys.stdin.readline())
    teams = []
    for i in range(team_count):
        i,j = sys.stdin.readline().strip().split(" ", 2)
        i,j = int(i), int(j)

        if i < 1000 or i > 1999:
            raise Exception("invalid Stockholm id")
        if j < 2000 or j > 2999:
            raise Exception("invalid London id")

        teams.append((i, j))
    return teams

def makeCombinations(teams, results):
    if len(teams) < 1:
        return results

    left,right = teams[0]

    new_results = []
    for result in results:
        r1 = result.copy()
        r1.add(left)
        new_results.append(r1)

        r2 = result.copy()
        r2.add(right)
        new_results.append(r2)

    return makeCombinations(teams[1:], new_results)

def findShortestSets(combinations, max_length):
    for i in range(max_length):
        results = [x for x in combinations if len(x) == i]
        if len(results) > 0:
            return results


def findSetWithId(sets, id):
    for x in sets:
        if id in x:
            return x

    return sets[0]
def main():
    teams = parseInput()

    combinations = makeCombinations(teams, [set()])

    shortestSets = findShortestSets(combinations, len(teams))
    winnerSet = findSetWithId(shortestSets, FRIEND)

    print len(winnerSet)
    for winner in winnerSet:
        print winner

    return 0

if __name__ == "__main__":
    sys.exit(main())