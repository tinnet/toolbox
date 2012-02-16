import random
import sys

TEAMS = int(sys.argv[1])

print TEAMS
for i in range(TEAMS):
    print random.randint(1000,1999), random.randint(2000,2999)
