#ifndef EXAMPLE_CALCULATOR_H
#define EXAMPLE_CALCULATOR_H

#include <string>

class Calculator
{
public:
    virtual ~Calculator() = default;
    virtual void solveEquation(const std::string& eqn) = 0;
};

#endif // EXAMPLE_CALCULATOR_H
