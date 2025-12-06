#ifndef BITCOIN_NODE_DATABASE_ARGS_H
#define BITCOIN_NODE_DATABASE_ARGS_H

class ArgsManager;
struct DBOptions;

namespace node {
void ReadDatabaseArgs(const ArgsManager& args, DBOptions& options);
} // namespace node

#endif // BITCOIN_NODE_DATABASE_ARGS_H
