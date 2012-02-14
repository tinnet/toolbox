#include "common.h"

void toLowerString(std::string &inString){
    // < ugly ...
    for (unsigned int i = 0; i < inString.length(); ++i)
    {
        inString[i]=tolower(inString[i]);
    } 
    // ugly ...>
};

void toUpperString(std::string &inString) {
    // < ugly ...
    for (unsigned int i = 0; i < inString.length(); ++i)
    {
        inString[i]=toupper(inString[i]);
    } 
    // ugly ...>
}
