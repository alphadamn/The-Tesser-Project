#!/bin/bash

# Define total nonce range (e.g., 0 to 4 billion)
START_NONCE=0
END_NONCE=4047121067

# Calculate the midpoint
MID_NONCE=$(( (START_NONCE + END_NONCE) / 2 ))

# Function to run GenesisH0 with a nonce range
run_miner() {
    INSTANCE_NAME=$1
    LOWER_BOUND=$2
    UPPER_BOUND=$3

    echo "Starting $INSTANCE_NAME from $LOWER_BOUND to $UPPER_BOUND"
    # Assuming GenesisH0 can take range parameters. You might need to modify it to accept them.
    ./GenesisH0 --start $LOWER_BOUND --end $UPPER_BOUND > "output_$INSTANCE_NAME.log" 2>&1 &
}

# Run two instances in parallel, splitting the work
run_miner "miner1" $START_NONCE $MID_NONCE
run_miner "miner2" $((MID_NONCE + 1)) $END_NONCE

# Wait for both background jobs to finish
wait

echo "Both mining instances have finished."
# You would then need to check the output files to see if either one was successful.