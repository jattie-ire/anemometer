dts=$(date "+%Y-%m-%d %H:%M:%S.$(date +%6N)")
echo $(date "+%Y-%m-%d %H:%M:%S.$(date +%6N)") Copy data to postgres server
find /home/jattie/log -type f -cmin -60 -exec scp {} weather@postgres.local:logfiles \;
dts=$(date "+%Y-%m-%d %H:%M:%S.$(date +%6N)")
echo $(date "+%Y-%m-%d %H:%M:%S.$(date +%6N)") purge older than 30 days
find /home/jattie/log -name '*.csv' -ctime +30 -exec rm {} \;
echo $(date "+%Y-%m-%d %H:%M:%S.$(date +%6N)") Processing completed

