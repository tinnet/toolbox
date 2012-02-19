#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

class TeamCountError(Exception):
    pass

class EmployeeId(Exception):
    pass

FRIEND = 1009

def parseInput():
    team_count = int(sys.stdin.readline().strip())
    if team_count < 1 or team_count > 10000:
        raise TeamCountError("between 1 and 10000 teams are allowed")

    employees = dict()
    teams = dict()
    for team_id in xrange(team_count):
        i,j = sys.stdin.readline().strip().split(" ", 2)
        i,j = int(i), int(j)

        if i < 1000 or i > 1999:
            raise EmployeeId("invalid Stockholm id")
        if j < 2000 or j > 2999:
            raise EmployeeId("invalid London id")

        teams[team_id] = (i,j)

        for id in [i,j]:
            if id in employees:
                employees[id].add(team_id)
            else:
                employees[id] = set([team_id])

    return teams,employees

def prune(employees, protect=None):
    employee_ids = employees.keys()
    result = set(employees.keys())

    for current_employee in employee_ids:
        for other_employee in employee_ids:
            # don't delete the protected employee
            if other_employee == protect:
                continue

            # don't delete ourself
            if current_employee == other_employee:
                continue

            # this employee has been deleted already, does not get to delete others
            if current_employee not in result:
                continue

            if employees[current_employee].issuperset(employees[other_employee]):
                result.remove(other_employee)

    return result

def main():
    teams, employees = parseInput()

    protected = prune(employees, FRIEND)
    fair =  prune(employees)

    if len(protected) <= len(fair):
        winners = protected
    else:
        winners = fair

    print len(winners)
    for winner in winners:
        print winner

    return 0

if __name__ == "__main__":
    sys.exit(main())