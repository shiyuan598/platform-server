#!/bin/bash
nohup node weread.js &
echo $! > pid.txt