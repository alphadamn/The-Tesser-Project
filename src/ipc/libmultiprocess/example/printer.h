#ifndef EXAMPLE_PRINTER_H
#define EXAMPLE_PRINTER_H

#include <string>

class Printer
{
public:
    virtual ~Printer() = default;
    virtual void print(const std::string& message) = 0;
};

#endif // EXAMPLE_PRINTER_H
