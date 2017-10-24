#!/bin/bash

docker run -it --rm \
    -v $(pwd):/mnt \
    vanandrew/postfreesurfer
