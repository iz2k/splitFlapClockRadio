#!/usr/bin/env bash
arecord -c2 -r 48000 -f S32_LE -t wav -V stereo | aplay