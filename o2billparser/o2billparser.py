# parses .csv files from o2 germany billing
# counts talked minutes ('sprache' in 'ART'), sms sent ('sms' in 'TARIFGRUPPE')
# ignores international minutes/sms
import csv
import glob
#import string

MYPATH = './data/*.CSV' # e.g. './mybills/*.csv'
MYDELIMITER = '|'

if __name__ == "__main__":
    FILENAMES = glob.glob(MYPATH)
    assert len(FILENAMES) > 0, "Error! No Files found (check path)"
    FILENAMES.sort()

    TOTALMINUTES = 0
    TOTALSMS = 0
    TOTALHOMEZONE = 0
    for filename in FILENAMES:
        csvfile = open(filename)
        reader = csv.DictReader(csvfile, delimiter=MYDELIMITER)
        smscount = 0
        timecount = dict(hours=0, minutes=0, seconds=0)
        homezonecount = 0
        for row in reader:
            if 'sprache' in str.lower(row['ART']):
                (h, m, s) = str.split(row['DAUER'], ':')
                timecount['hours'] += int(h)
                timecount['minutes'] += int(m)
                timecount['seconds'] += int(s)
                if 'homezone' in str.lower(row['TARIFGRUPPE']):
                    homezonecount += int(m) + (int(h) * 60) + (int(s) / 60)
            if 'sms' in str.lower(row['TARIFGRUPPE']):
                smscount = smscount + 1
        minutes = timecount['minutes'] + \
                  (timecount['hours'] * 60)  + \
                  (timecount['seconds'] / 60)
        TOTALMINUTES += minutes
        TOTALSMS += smscount
        TOTALHOMEZONE += homezonecount
        print "%s: %3d Minutes %3d SMS (%3d Minutes in Homezone)"  % \
            (filename.rpartition('/')[2], minutes, smscount, homezonecount)
        assert minutes >= homezonecount, \
            "Error! More minutes in homezone than total?"
    # the cool .format prints only work in python 2.6 ...
    print('Total  :{0:4} Minutes and {1:4} SMS in {2} Months ({3:4} Minutes in Homezone)'.format(TOTALMINUTES, TOTALSMS, len(FILENAMES), TOTALHOMEZONE))
    print('Average:{0:4} Minutes and {1:4} SMS per Month'.format(TOTALMINUTES / len(FILENAMES), TOTALSMS / len(FILENAMES)))
    # ... and since that isn't in debian stable yet... i added "old" prints
    #print('Total   '+str(totalminutes)+' Minutes '+str(totalsms)+' SMS in '+str(len(files))+' Months ('+str(totalhomezone)+' Minutes in Homezone)')
    #print('Average '+str(totalminutes/len(files))+' Minutes '+str(totalsms/len(files))+' SMS per Month')
