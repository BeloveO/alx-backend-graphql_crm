#!/bin/bash
# this script should delete customers with no orders since a year ago

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="$(basename "$(dirname "$(dirname "$SCRIPT_DIR")")")"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DELETION_RESULT=""
# log the result
if [ "$DELETION_RESULT" -eq 0 ]; then
    echo "[$TIMESTAMP] Successfully deleted inactive customers." >> /tmp/customer_cleanup_log.txt
else
    echo "[$TIMESTAMP] Failed to delete inactive customers." >> /tmp/customer_cleanup_log.txt
fi
