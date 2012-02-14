#include "cWoerterbuch.h"

cWoerterbuch::cWoerterbuch() {
    wordCount = 0;
    collisions = 0;
};

cWoerterbuch::~cWoerterbuch() {
    for (std::map<unsigned long, hashElement>::iterator destroya = hashTabelle.begin();
         destroya != hashTabelle.end();
         ++destroya)
    {
        hashElement *thisEle, *nextEle;
        thisEle = &destroya->second;
        nextEle = destroya->second.next;

        while(nextEle != NULL) {
            delete(thisEle);
            thisEle = nextEle;
            nextEle = thisEle->next;
        }
    } 
}

unsigned long cWoerterbuch::hashWord (std::string curWord) {
    unsigned long myhash = fnv_32_str(curWord.c_str(), FNV1_32_INIT);
    return(myhash);
};

void cWoerterbuch::insert( std::string curWord ) {
    unsigned long curHash = hashWord(curWord);

    if (hashTabelle.count(curHash) == 0) {
        // new word found
        hashElement *curElement = new hashElement;
        curElement->theWord = curWord;
        curElement->theCount = 1;
        curElement->next = NULL;
        hashTabelle[curHash] = *curElement;
        delete(curElement);
        wordCount++;
    } else {
        // collissionsbehandlung
        hashElement *checkEle = &hashTabelle[curHash];

        while(true) {
            // durchläuft verkette Liste und sucht das passende Wort
            if (checkEle->theWord != curWord) {
                if (checkEle->next != NULL) {
                    checkEle = checkEle->next;
                } else {
                    // Ende der verketten Liste, kein passendes gefunden, neues anhängen
                    hashElement *newElement = new hashElement;
                    newElement->theWord = curWord;
                    newElement->theCount = 1;
                    newElement->next = NULL;
                    checkEle->next = newElement;
                    delete(newElement);
                    collisions++;
                    break;
                }
            } else {
                    // wort gefunden, zähler erhöhen
                    checkEle->theCount++;
                    break;
            }

            //std::cout << hashTabelle[curHash].theWord << " - " << hashTabelle[curHash].theCount << std::endl;
            //std::cout << curWord << " - "<< curHash << std::endl;
       }
    }
};


unsigned int cWoerterbuch::lookup( std::string &curWord ) {
    /* ich tu noch nix ;P */
    return(0);
};

unsigned long cWoerterbuch::getCount ( const std::string &curWord) {
    unsigned long curHash = hashWord(curWord);
    // gibts es Einträge in der hashtabelle?
    if ( !(hashTabelle.count(curHash) == 0) ) {
        hashElement *checkElement = &hashTabelle[curHash];
        while (true) {
            if (checkElement->theWord == curWord) {
                return (checkElement->theCount);
            } else {
                if (checkElement->next != NULL) {
                    checkElement = checkElement->next;
                } else {
                    // gesuchtes Wort nicht im wörterbuch
                    return 0;
                }
            }
        }
    } else {
        // feld noch leer
        return 0;
    }   
};

void cWoerterbuch::printall () {
    std::cout << std::endl << "Printing entire hashtable (warning: this could take a while)..." << std::endl;
    for (std::map<unsigned long, hashElement>::iterator print = hashTabelle.begin();
         print != hashTabelle.end();
         ++print)
    {
        std::cout << print->first << " : " << print->second.theWord << std::endl;
    } 
}
