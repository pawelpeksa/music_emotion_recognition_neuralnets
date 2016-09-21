#!/bin/sh
# usage: svn st | x 2 | xargs rm
col=$1
shift
awk -v col="$col" '{print $col}' "${@--}"