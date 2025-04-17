#!/bin/sh
set -e

# Start API
/app/api/start_api.sh &

# Start FTP sync process
while true; do
    lftp -u ${USERNAME},${PASSWORD} -e "mirror --delete --verbose ${ROOT_PATH} /share/ftp_shared; quit" ${HOST}
    find /share/ftp_shared -type f -mmin +$((SHARE_DURATION/60)) -delete
    sleep 300
done
