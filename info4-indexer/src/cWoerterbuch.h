#include <iostream>
#include <fstream>
#include <map>
#include <string>
#include <stdlib.h>

#include "fnv.h"

class cWoerterbuch {
    private:
	    struct hashElement {
		    std::string theWord;
            unsigned long theCount;
            hashElement *next;
	    }; 
	    std::map<unsigned long, hashElement> hashTabelle;

    public:
        unsigned long wordCount;
        unsigned int  collisions;
        
        cWoerterbuch();
        ~cWoerterbuch();
        
        unsigned long hashWord (std::string curWord);
        void          insert   (std::string curWord);
        unsigned int  lookup   (std::string &curWord);
	    unsigned long getCount (const std::string &curWord);
	    void          printall ();
};
