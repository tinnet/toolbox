#include <iostream>
#include <fstream>
#include <list>
#include <string>

#include "cWoerterbuch.h"
#include "common.h"

#define READ_BUFFER_SIZE 4096
#define TRENNZEICHEN " ,.:;!?+-*~@/_(){}[]<>&\"\t\n\r\\"

class cIndexer {
    private:
        std::string  restbuffer;
        std::string  separators;
        cWoerterbuch *thisWB;
    public:
                      cIndexer   (cWoerterbuch *WB);
        int           loadFile   (const std::string &curPath);
        void          indexBlock (const std::string &inBuffer);
        void          splitString(const std::string &inString, std::list<std::string> &words);
        std::string   cleanWord  (std::string inString);
        bool          checkIfText(const std::string &curPath);
        unsigned long totalwords;
};
