import datetime
import itertools
import sys

MINIMUM_DATE = datetime.date(2000,01,01)
MAXIMUM_DATE = datetime.date(2999,12,31)

def parseDate(dateString):
    parts = dateString.split("/")
    if len(parts) != 3:
        raise Exception("wrong amount of parts")
    try:
        parts = map(int, parts)
    except ValueError:
        raise Exception("non integer part")

    possible_dates = []
    for permutation in itertools.permutations(parts):
        try:
            date = datetime.date(*permutation)

            if date < MINIMUM_DATE:
                date = date.replace(year=date.year+MINIMUM_DATE.year)

            if date > MAXIMUM_DATE:
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
