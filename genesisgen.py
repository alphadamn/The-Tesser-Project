import concurrent
import hashlib, binascii, struct, array, os, time, sys, optparse
import multiprocessing
import threading
from concurrent.futures import ProcessPoolExecutor

import scrypt

from construct import *

nonce_counter = None

#def main():
#     options = get_args()
#
#     algorithm = get_algorithm(options)
#
#     input_script  = create_input_script(options.timestamp)
#     output_script = create_output_script(options.pubkey)
#     # hash merkle root is the double sha256 hash of the transaction(s)
#     tx = create_transaction(input_script, output_script,options)
#     hash_merkle_root = hashlib.sha256(hashlib.sha256(tx).digest()).digest()
#     print_block_info(options, hash_merkle_root)
#
#     block_header        = create_block_header(hash_merkle_root, options.time, options.bits, options.nonce)
#     genesis_hash, nonce = generate_hash(block_header, algorithm, options.nonce, options.bits)
#     announce_found_genesis(genesis_hash, nonce)
# def main():
#     options = get_args()
#     algorithm = get_algorithm(options)
#
#     input_script  = create_input_script(options.timestamp)
#     output_script = create_output_script(options.pubkey)
#     tx = create_transaction(input_script, output_script,options)
#     hash_merkle_root = hashlib.sha256(hashlib.sha256(tx).digest()).digest()
#     print_block_info(options, hash_merkle_root)
#
#     block_header = create_block_header(hash_merkle_root, options.time, options.bits, options.nonce)
#
#     # Use multithreaded version instead of original
#     genesis_hash, nonce = generate_hash_parallel(block_header, algorithm, options.nonce, options.bits, num_threads=8)
#
#     announce_found_genesis(genesis_hash, nonce)

def main():
    options = get_args()
    algorithm = get_algorithm(options)

    input_script  = create_input_script(options.timestamp)
    output_script = create_output_script(options.pubkey)
    tx = create_transaction(input_script, output_script, options)
    hash_merkle_root = hashlib.sha256(hashlib.sha256(tx).digest()).digest()
    print_block_info(options, hash_merkle_root)

    block_header = create_block_header(hash_merkle_root, options.time, options.bits, options.nonce)

    # Use the enhanced version with hashrate display
    genesis_hash, nonce = generate_hash_with_hashrate(
        block_header,
        algorithm,
        options.nonce,
        options.bits,
        num_threads=multiprocessing.cpu_count()
    )

    if genesis_hash:
        announce_found_genesis(genesis_hash, nonce)
    else:
        print("Failed to find genesis block")

def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--time", dest="time", default=int(time.time()),
                      type="int", help="the (unix) time when the genesisblock is created")
    parser.add_option("-z", "--timestamp", dest="timestamp", default="The Times 03/Jan/2009 Chancellor on brink of second bailout for banks",
                      type="string", help="the pszTimestamp found in the coinbase of the genesisblock")
    parser.add_option("-n", "--nonce", dest="nonce", default=0,
                      type="int", help="the first value of the nonce that will be incremented when searching the genesis hash")
    parser.add_option("-a", "--algorithm", dest="algorithm", default="SHA256",
                      help="the PoW algorithm: [SHA256|scrypt|X11|X13|X15]")
    parser.add_option("-p", "--pubkey", dest="pubkey", default="04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f",
                      type="string", help="the pubkey found in the output script")
    parser.add_option("-v", "--value", dest="value", default=5000000000,
                      type="int", help="the value in coins for the output, full value (exp. in bitcoin 5000000000 - To get other coins value: Block Value * 100000000)")
    parser.add_option("-b", "--bits", dest="bits",
                      type="int", help="the target in compact representation, associated to a difficulty of 1")

    (options, args) = parser.parse_args()
    if not options.bits:
        if options.algorithm == "scrypt" or options.algorithm == "X11" or options.algorithm == "X13" or options.algorithm == "X15":
            options.bits = 0x1e0ffff0
        else:
            options.bits = 0x1d00ffff
    return options

def get_algorithm(options):
    supported_algorithms = ["SHA256", "scrypt", "X11", "X13", "X15"]
    if options.algorithm in supported_algorithms:
        return options.algorithm
    else:
        sys.exit("Error: Given algorithm must be one of: " + str(supported_algorithms))

def create_input_script(psz_timestamp):
    psz_prefix = ""
    #use OP_PUSHDATA1 if required
    if len(psz_timestamp) > 76: psz_prefix = '4c'

    script_prefix = '04ffff001d0104' + psz_prefix + chr(len(psz_timestamp)).encode().hex()
    print((script_prefix + psz_timestamp.encode().hex()))
    return bytes.fromhex(script_prefix + psz_timestamp.encode().hex())


def create_output_script(pubkey):
    script_len = '41'
    OP_CHECKSIG = 'ac'
    return bytes.fromhex(script_len + pubkey + OP_CHECKSIG)

def create_transaction(input_script, output_script,options):
    transaction = Struct("transaction",
                         Bytes("version", 4),
                         Byte("num_inputs"),
                         StaticField("prev_output", 32),
                         UBInt32('prev_out_idx'),
                         Byte('input_script_len'),
                         Bytes('input_script', len(input_script)),
                         UBInt32('sequence'),
                         Byte('num_outputs'),
                         Bytes('out_value', 8),
                         Byte('output_script_len'),
                         Bytes('output_script',  0x43),
                         UBInt32('locktime'))

    tx = transaction.parse(b'\x00'*(127 + len(input_script)))
    tx.version           = struct.pack('<I', 1)
    tx.num_inputs        = 1
    tx.prev_output       = struct.pack('<qqqq', 0,0,0,0)
    tx.prev_out_idx      = 0xFFFFFFFF
    tx.input_script_len  = len(input_script)
    tx.input_script      = input_script
    tx.sequence          = 0xFFFFFFFF
    tx.num_outputs       = 1
    tx.out_value         = struct.pack('<q' ,options.value)#0x000005f5e100)#012a05f200) #50 coins
    #tx.out_value         = struct.pack('<q' ,0x000000012a05f200) #50 coins
    tx.output_script_len = 0x43
    tx.output_script     = output_script
    tx.locktime          = 0
    return transaction.build(tx)


def create_block_header(hash_merkle_root, time, bits, nonce):
    block_header = Struct("block_header",
                          Bytes("version",4),
                          Bytes("hash_prev_block", 32),
                          Bytes("hash_merkle_root", 32),
                          Bytes("time", 4),
                          Bytes("bits", 4),
                          Bytes("nonce", 4))

    genesisblock = block_header.parse(b'\x00'*80)
    genesisblock.version          = struct.pack('<I', 1)
    genesisblock.hash_prev_block  = struct.pack('<qqqq', 0,0,0,0)
    genesisblock.hash_merkle_root = hash_merkle_root
    genesisblock.time             = struct.pack('<I', time)
    genesisblock.bits             = struct.pack('<I', bits)
    genesisblock.nonce            = struct.pack('<I', nonce)
    return block_header.build(genesisblock)


# https://en.bitcoin.it/wiki/Block_hashing_algorithm
# def generate_hash(data_block, algorithm, start_nonce, bits):
#     print('Searching for genesis hash..')
#     nonce           = start_nonce
#     last_updated    = time.time()
#     # https://en.bitcoin.it/wiki/Difficulty
#     target = (bits & 0xffffff) * 2**(8*((bits >> 24) - 3))
#
#     while True:
#         sha256_hash, header_hash = generate_hashes_from_block(data_block, algorithm)
#         last_updated             = calculate_hashrate(nonce, last_updated)
#         if is_genesis_hash(header_hash, target):
#             if algorithm == "X11" or algorithm == "X13" or algorithm == "X15":
#                 return (header_hash, nonce)
#             return (sha256_hash, nonce)
#         else:
#             nonce      = nonce + 1
#             data_block = data_block[0:len(data_block) - 4] + struct.pack('<I', nonce)


def generate_hashes_from_block(data_block, algorithm):
    sha256_hash = hashlib.sha256(hashlib.sha256(data_block).digest()).digest()[::-1]
    header_hash = ""
    if algorithm == 'scrypt':
        header_hash = scrypt.hash(data_block,data_block,1024,1,1,32)[::-1]
    elif algorithm == 'SHA256':
        header_hash = sha256_hash
    elif algorithm == 'X11':
        try:
            exec('import %s' % "xcoin_hash")
        except ImportError:
            sys.exit("Cannot run X11 algorithm: module xcoin_hash not found")
        header_hash = xcoin_hash.getPoWHash(data_block)[::-1]
    elif algorithm == 'X13':
        try:
            exec('import %s' % "x13_hash")
        except ImportError:
            sys.exit("Cannot run X13 algorithm: module x13_hash not found")
        header_hash = x13_hash.getPoWHash(data_block)[::-1]
    elif algorithm == 'X15':
        try:
            exec('import %s' % "x15_hash")
        except ImportError:
            sys.exit("Cannot run X15 algorithm: module x15_hash not found")
        header_hash = x15_hash.getPoWHash(data_block)[::-1]
    return sha256_hash, header_hash


# def generate_hash_parallel(data_block, algorithm, start_nonce, bits, num_threads=None):
#     global nonce_counter
#     print('Searching for genesis hash with {} threads..'.format(num_threads or multiprocessing.cpu_count()))
#
#     if num_threads is None:
#         num_threads = multiprocessing.cpu_count()
#
#     # Shared variables
#     found_event = threading.Event()
#     result_container = [None]
#     nonce_counter = start_nonce
#     nonce_lock = threading.Lock()
#     last_updated = time.time()
#     target = (bits & 0xffffff) * 2**(8*((bits >> 24) - 3))
#
#     def worker(thread_id):
#         global nonce_counter
#         nonlocal last_updated
#         local_nonce = start_nonce + thread_id
#
#         while not found_event.is_set():
#             with nonce_lock:
#                 current_nonce = nonce_counter
#                 nonce_counter += num_threads
#
#             # Update data block with current nonce
#             current_data_block = data_block[0:len(data_block) - 4] + struct.pack('<I', current_nonce)
#
#             sha256_hash, header_hash = generate_hashes_from_block(current_data_block, algorithm)
#
#             # Update hashrate display (only from thread 0 to avoid messy output)
#             if thread_id == 0 and current_nonce % 1000000 == 999999:
#                 now = time.time()
#                 hashrate = round(1000000/(now - last_updated))
#                 generation_time = round(pow(2, 32) / hashrate / 3600, 1)
#                 sys.stdout.write("\r{} hash/s, estimate: {} h".format(str(hashrate), str(generation_time)))
#                 sys.stdout.flush()
#                 last_updated = now
#
#             if is_genesis_hash(header_hash, target):
#                 with nonce_lock:
#                     if not found_event.is_set():
#                         found_event.set()
#                         if algorithm == "X11" or algorithm == "X13" or algorithm == "X15":
#                             result_container[0] = (header_hash, current_nonce)
#                         else:
#                             result_container[0] = (sha256_hash, current_nonce)
#                 return
#
#     # Start worker threads
#     threads = []
#     for i in range(num_threads):
#         thread = threading.Thread(target=worker, args=(i,))
#         thread.daemon = True
#         thread.start()
#         threads.append(thread)
#
#     # Wait for any thread to find the solution
#     found_event.wait()
#
#     # Give threads a moment to finish
#     time.sleep(0.1)
#
#     return result_container[0]

def is_genesis_hash(header_hash, target):
    return int(header_hash.hex(), 16) < target


def calculate_hashrate(nonce, last_updated):
    if nonce % 1000000 == 999999:
        now             = time.time()
        hashrate        = round(1000000/(now - last_updated))
        generation_time = round(pow(2, 32) / hashrate / 3600, 1)
        sys.stdout.write("\r%s hash/s, estimate: %s h"%(str(hashrate), str(generation_time)))
        sys.stdout.flush()
        return now
    else:
        return last_updated


def print_block_info(options, hash_merkle_root):
    print("algorithm: "    + (options.algorithm))
    print("merkle hash: "  + hash_merkle_root[::-1].hex())
    print("pszTimestamp: " + options.timestamp)
    print("pubkey: "       + options.pubkey)
    print("time: "         + str(options.time))
    print("bits: "         + str(hex(options.bits)))


def announce_found_genesis(genesis_hash, nonce):
    print("genesis hash found!")
    print("nonce: "        + str(nonce))
    print("genesis hash: " + genesis_hash.hex())


# # GOGOGO!
# main()
import threading
import multiprocessing
import time
import struct
import hashlib
import sys
from collections import deque

def generate_hash_with_hashrate(data_block, algorithm, start_nonce, bits, num_threads=None):
    if num_threads is None:
        num_threads = multiprocessing.cpu_count()

    print(f'Searching for genesis hash with {num_threads} threads...')

    target = (bits & 0xffffff) * 2**(8*((bits >> 24) - 3))
    data_block_template = data_block[0:len(data_block) - 4]

    # Shared variables for hashrate calculation
    found_event = threading.Event()
    result_queue = []
    result_lock = threading.Lock()

    # Hashrate tracking
    total_hashes = 0
    hashrate_lock = threading.Lock()
    start_time = time.time()

    # For smooth hashrate calculation
    hashrate_history = deque(maxlen=10)  # Keep last 10 measurements
    last_hash_count = 0

    # Hashrate display thread
    def hashrate_reporter():
        nonlocal last_hash_count
        while not found_event.is_set():
            time.sleep(1.0)  # Update every second
            with hashrate_lock:
                current_hashes = total_hashes
                hashes_this_second = current_hashes - last_hash_count
                last_hash_count = current_hashes

            # Calculate hashrate (hashes per second)
            elapsed = time.time() - start_time
            current_hashrate = int(total_hashes / elapsed) if elapsed > 0 else 0

            # Add to history for smoothing
            hashrate_history.append(hashes_this_second)
            avg_hashrate = sum(hashrate_history) / len(hashrate_history) if hashrate_history else 0

            # Format display
            if avg_hashrate > 1000000:
                display_rate = f"{avg_hashrate/1000000:.2f} MH/s"
            elif avg_hashrate > 1000:
                display_rate = f"{avg_hashrate/1000:.2f} kH/s"
            else:
                display_rate = f"{avg_hashrate:.0f} H/s"

            # Show progress
            sys.stdout.write(f"\rHashrate: {display_rate} | Total: {total_hashes:,} | Elapsed: {int(elapsed)}s")
            sys.stdout.flush()

    # Worker thread function
    def worker(thread_id, batch_size=10000):
        nonlocal total_hashes
        local_hashes = 0
        nonce = start_nonce + thread_id

        while not found_event.is_set():
            # Process a batch of nonces
            batch_hashes = 0
            for i in range(batch_size):
                if found_event.is_set():
                    break

                current_data_block = data_block_template + struct.pack('<I', nonce)
                sha256_hash, header_hash = generate_hashes_from_block(current_data_block, algorithm)
                batch_hashes += 1

                if is_genesis_hash(header_hash, target):
                    with result_lock:
                        if not found_event.is_set():
                            found_event.set()
                            result_hash = sha256_hash if algorithm == "SHA256" else header_hash
                            result_queue.append((result_hash, nonce))
                    return

                nonce += num_threads

            # Update global hash count
            local_hashes += batch_hashes
            if local_hashes >= 1000:  # Update global counter periodically to reduce lock contention
                with hashrate_lock:
                    total_hashes += local_hashes
                local_hashes = 0

        # Don't forget to add remaining local hashes
        if local_hashes > 0:
            with hashrate_lock:
                total_hashes += local_hashes

    # Start hashrate reporter thread
    reporter_thread = threading.Thread(target=hashrate_reporter)
    reporter_thread.daemon = True
    reporter_thread.start()

    # Start worker threads
    worker_threads = []
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(i,))
        t.daemon = True
        t.start()
        worker_threads.append(t)

    print("Mining started. Press Ctrl+C to stop.")

    try:
        # Wait for any worker to find solution
        while not found_event.is_set():
            time.sleep(0.1)

            # Check if all threads died (shouldn't happen normally)
            alive_count = sum(1 for t in worker_threads if t.is_alive())
            if alive_count == 0 and not found_event.is_set():
                print("\nAll worker threads stopped unexpectedly!")
                break

    except KeyboardInterrupt:
        print("\n\nMining interrupted by user!")
        found_event.set()

    # Wait for threads to finish
    for t in worker_threads:
        t.join(timeout=1.0)

    # Final hashrate calculation
    if total_hashes > 0:
        total_time = time.time() - start_time
        final_hashrate = total_hashes / total_time
        if final_hashrate > 1000000:
            display_final = f"{final_hashrate/1000000:.2f} MH/s"
        elif final_hashrate > 1000:
            display_final = f"{final_hashrate/1000:.2f} kH/s"
        else:
            display_final = f"{final_hashrate:.0f} H/s"

        print(f"\nFinal statistics:")
        print(f"  Total hashes: {total_hashes:,}")
        print(f"  Total time: {total_time:.1f}s")
        print(f"  Average hashrate: {display_final}")

    if result_queue:
        print("\n🎉 Genesis block found!")
        return result_queue[0]
    else:
        print("\n❌ No solution found (try increasing nonce range)")
        return None

main()