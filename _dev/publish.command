#!/bin/bash
cd "$(dirname "$0")/.." || exit 1
./_dev/publish.sh
echo
echo "Live site: https://therapistsupport.org/"
read -r -p "Press return to close." _
