#include "cIndexer.h"

cIndexer::cIndexer( cWoerterbuch *WB) {
    separators  = TRENNZEICHEN;
    thisWB = WB;
    restbuffer = "";
    totalwords = 0;
};

int cIndexer::loadFile( const std::string &curPath ) {
    if (checkIfText(curPath)) {
        // filestream erzeugen
        std::ifstream curFile(curPath.c_str(), std::ios_base::in | std::ios_base::binary);
        if (!curFile) {
            std::cout << "Error while Opening file" << curPath;
            exit(1);
        }
        // Datei blockweise einlesen
        while (!curFile.eof()) {
            char buffer[READ_BUFFER_SIZE+1] ="";
            curFile.read(buffer, READ_BUFFER_SIZE);
            buffer[READ_BUFFER_SIZE] = 0; // nullterminiert
            // und indizieren
            indexBlock(buffer);     
            //cout << buffer;
        }
        curFile.close(); 
    } else {
        std::cout << "The File you gave me is not a textfile, sorry." << std::endl <<std::endl;
        return -1;
    }
    return 0;
};

void cIndexer::indexBlock( const std::string &inBuffer ) {
    //cout << endl << "In cIndexer::indexBlock " << inBuffer << endl;
    std::list<std::string> words;
    splitString(inBuffer, words);
    //cout << "Vor Übertragchek: " << inBuffer << endl; 
    
    // Check ob wir durch Blockbildung ein Wort getrennt haben im letzten Block
    if ( (restbuffer.length() > 0) && (separators.find(inBuffer[0]) == std::string::npos) ) {
        std::string temp = words.front();
        words.pop_front();
        words.push_front(restbuffer + temp);
        restbuffer = "";
    }
    // bis auf das letzte wort alle ins Wörterbuch
    while (words.size() > 1) {
        // nur wörter über 2 und unter 32 Zeichen länge
        // (3 Zeichen können schon sinnvoll sein ARD, ZDF ...)
        if ( (words.front().length() > 2) && (words.front().length() < 33)) {
            thisWB->insert(words.front());
            totalwords++;
        }
        words.pop_front();
    }
    
    // Check ob Block "sauber" endet
    if ( (separators.find(inBuffer[inBuffer.length() - 1]) != std::string::npos) ) {
        // wenn ja, letztes Wort auchnoch ins Wörterbuch
        thisWB->insert(words.front());
        words.pop_front();
        restbuffer = "";
    } else {
        // ansonsten in den "übertrag" damit
        restbuffer = words.front();
        words.pop_front();
    };
}; 

void cIndexer::splitString(const std::string &inString, std::list<std::string> &words) {
    //cout << endl << "In cIndexer::splitString" << endl;
    //std::cout << "PreSplit: "<< inString << std::endl;
    size_t n     = inString.length();
    size_t start = inString.find_first_not_of(separators);  

    while (start < n) {
        size_t stop = inString.find_first_of(separators, start);
        if (stop > n) stop = n;
        words.push_back ( cleanWord( inString.substr(start, stop-start) ) );
        start = inString.find_first_not_of(separators, stop+1);
    }

    //debugausgabe
    /*std::cout << "PostSplit: ";
    for (int i = 0; i < words.size(); i++) {
        std::cout << words.front() << " - ";
        words.push_back(words.front());
        words.pop_front();
    }
    std::cout << std::endl; */

};

std::string cIndexer::cleanWord(std::string inString) {
    //TODO zusätzliche "säuberung" des Wortes, spezialbehandlung für Datum/Zahlen html usw.
    toLowerString(inString);
    return(inString);
}

bool cIndexer::checkIfText(const std::string &curPath) {
    // TODO check nach magic bytes!

    std::string fileExt = curPath.substr(curPath.find_last_of("."));

    if ( // Video
         (fileExt == ".avi") || (fileExt == ".mpg") || (fileExt == ".mpeg")|| (fileExt == ".ogm") ||
         (fileExt == ".mkv") ||
         // Audio
         (fileExt == ".mp3") || (fileExt == ".wav") || (fileExt == ".ogg") ||
         // Images
         (fileExt == ".jpg") || (fileExt == ".jpeg")|| (fileExt == ".bmp") || (fileExt == ".gif") ||
         (fileExt == ".png") ||
         // Archive
         (fileExt == ".rar") || (fileExt == ".zip") || (fileExt == ".gz")  || (fileExt == ".z")   ||
         (fileExt == ".bz2") || (fileExt == ".ace") || (fileExt == ".arj") ||
         // Sonstiges
         (fileExt == ".exe") || (fileExt == ".pdf") || (fileExt == ".ps")
       ) { 
             return(false);
         } else {
             return(true);
         };
}
