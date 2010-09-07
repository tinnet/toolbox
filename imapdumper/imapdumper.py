#!/usr/bin/python

import imaplib,re

##### SETUP HERE

IMAP_SERVER = 'SETUP'
IMAP_USER = 'SETUP'
IMAP_PW = 'SETUP'
IMAP_BOX = 'SETUP' # subdirs often are INBOX.DIR!

##### DONT TOUCH ANYTHING BELOW HERE

# create connection
M = imaplib.IMAP4(IMAP_SERVER)
M.login(IMAP_USER, IMAP_PW)

# select mailbox
M.select(IMAP_BOX)
_, data = M.search(None, 'ALL')

# loop over all messages
for num in data[0].split():
    _, data = M.fetch(num,'(BODY.PEEK[HEADER.FIELDS (FROM)])')
    #print(data)
    sender = (data[0])[1]
    #print(sender)
    matches = re.search('\s<?(\S*@[^\s>]*)>?\s', sender)

    print(matches.group(1))
# close & flush deleted
M.close()
M.logout()
        
