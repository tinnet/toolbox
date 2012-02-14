import datetime
import itertools
import sys

MINIMUM_DATE = datetime.date(2000,01,01)
MAXIMUM_DATE = datetime.date(2999,12,31)

def parseDate(dateString):
    parts = map(int, dateString.split("/", 3))

    possible_dates = []
    for permutation in itertools.permutations(parts):
        try:
            if permutation[0] < MINIMUM_DATE.year:
                permutation = (permutation[0]+MINIMUM_DATE.year, permutation[1],permutation[2])

            date = datetime.date(*permutation)

            if date < MINIMUM_DATE or date > MAXIMUM_DATE:
                continue

            possible_dates.append(date)
        except ValueError:
            pass

    if len(possible_dates) < 1:
        raise Exception("no possible dates")

    return min(possible_dates).isoformat()

def main():
    for line in sys.stdin:
        try:
            print parseDate(line.strip())
        except Exception:
            print "%s is illegal" % line.strip()

    return 0

if __name__ == "__main__":
    sys.exit(main())
