#ifndef BITCOIN_MAPPORT_H
#define BITCOIN_MAPPORT_H

static constexpr bool DEFAULT_NATPMP = true;

void StartMapPort(bool enable);
void InterruptMapPort();
void StopMapPort();

#endif // BITCOIN_MAPPORT_H
