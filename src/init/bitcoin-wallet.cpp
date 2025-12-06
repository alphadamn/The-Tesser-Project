#include <interfaces/init.h>

#include <memory>

namespace interfaces {
std::unique_ptr<Init> MakeWalletInit(int argc, char* argv[], int& exit_status)
{
    return std::make_unique<Init>();
}
} // namespace interfaces
