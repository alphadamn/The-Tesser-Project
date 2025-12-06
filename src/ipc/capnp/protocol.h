#ifndef BITCOIN_IPC_CAPNP_PROTOCOL_H
#define BITCOIN_IPC_CAPNP_PROTOCOL_H

#include <memory>

namespace ipc {
class Protocol;
namespace capnp {
std::unique_ptr<Protocol> MakeCapnpProtocol();
} // namespace capnp
} // namespace ipc

#endif // BITCOIN_IPC_CAPNP_PROTOCOL_H
