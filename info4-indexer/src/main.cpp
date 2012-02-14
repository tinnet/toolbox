#include <iostream>
#include <string>
#include <stdlib.h>

#ifdef WIN32
#include <Windows.h>
#endif

#include "common.h"
#include "cIndexer.h"

int main(int argc, char *argv[])
{
    if (argc != 2) {
        std::cout << "Please specify exactly one parameter, the filename, if necessary with the full path." << std::endl;
        system("PAUSE");
        return 1;
    }

    std::string curFilePath = argv[1]; // kompletter Dateiname mit Pfad
    std::string curFileName = curFilePath.substr( curFilePath.find_last_of("\\") + 1 ); // nur Dateiname

    std::cout << "Working real hard ..." << std::endl << std::endl;
    
#ifdef WIN32
    // für die Perfomancemessung
    long long frequency, startTime, stopTime;
    double timeTaken, timeScale;
    bool counterAvailable = false;
    // falls vorhanden den richtig schnellen timer
    if ( QueryPerformanceFrequency( (LARGE_INTEGER*) &frequency) ) {
        counterAvailable = true;
        timeScale = 1.0/frequency;
        QueryPerformanceCounter( (LARGE_INTEGER*) &startTime);
    } else  {
        // sonst den "langsamen" (auflösung 1ms)
        startTime = GetTickCount();
        timeScale = 0.001;
    }
#endif

    cWoerterbuch *myWoerterbuch = new cWoerterbuch();
    cIndexer *myIndexer = new cIndexer(myWoerterbuch);
    
    int myLoadResult = myIndexer->loadFile(argv[1]);
    
#ifdef WIN32
if (counterAvailable) {
        QueryPerformanceCounter( (LARGE_INTEGER*) &stopTime);
    } else {
        stopTime = GetTickCount();
    }
    
    timeTaken = ( stopTime - startTime ) * timeScale;
#else
    double timeTaken = 0;
#endif
    if (myLoadResult < 0) return -1;

    std::cout << "It took " << timeTaken << " seconds to index " << curFileName << std::endl;
    std::cout << "I found " << myWoerterbuch->wordCount << " unique Words in a total of "
                            << myIndexer->totalwords << " Words." << std::endl;
    std::cout << "I had "   << myWoerterbuch->collisions << " Collisions." << std::endl;
    

    while (true) {
        std::cout << std::endl;
        std::cout << "The following commands are available:" << std::endl <<
            "\"getCount WORD\" to view how many times i found WORD" << std::endl <<
            "\"printit\" to print the entire hashtable in format $HASH : $WORD." << std::endl <<
            "\"exit\" to quit the program (this will discard the index!)" << std::endl << std::endl;

        std::cout << "my master? > ";

        std::string inString;
        
        char inBuffer[255];
        std::cin.getline(inBuffer,256);
        inString = inBuffer;
        toLowerString(inString);
        std::string command = inString.substr( 0, inString.find_first_of(' ') );
        std::string commandParam = inString.substr( inString.find_first_of(' ')+1,inString.length() );

        if (command == "exit") {
            break;
        } 

        if (command == "getcount") {
            std::cout << std::endl << "I found \"" << commandParam <<  "\" " << myWoerterbuch->getCount(commandParam) << " Times." << std::endl;
            continue;
        } 
        if (command == "printit") {
            myWoerterbuch->printall();
            continue;
        } 
        std::cout << "Sorry, i couldn't understand that command" << std::endl;
        
    }
    
    delete(myWoerterbuch);
    delete(myIndexer);

    return 0;
}
