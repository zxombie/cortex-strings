#!/bin/bash
#
# Benchmark all variants of all functions

# memcpy: 9.905206 s for 10000000 calls to memcpy of 3328 bytes.  ~3204.202 MB/s
# To run for 10 s, transfer 30 GB.  So loops is 30e9 / size
for t in memcpy memset memchr strcpy strlen strcmp strchr bounce; do
    for variant in try-all try-bionic try-csl try-glibc try-newlib try-none try-plain; do
        #for size in 256 512 1024 2048 4096 8192 16384 $(seq 4 4 128); do
        for size in $(seq 4 4 128); do
            if [[ $size -le 128 ]]; then
                loops=$(( 250000000 - 1000000 * $size ))
            else
                loops=$(( 30000000000 / $size ))
            fi
            ./$variant -t $t -c $size -l $loops
        done
    done
done
250000000 - 1000000*size
