#!/bin/sh
# wait-for-mysql.sh

set -e
  
host="$1"
shift
cmd="$@"

until echo '\q' | mysql --host=$host --user=$MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE; do
    >&2 echo "MySQL is unavailable - sleeping"
    sleep 1
done

>&2 echo "MySQL is up - executing command"
exec $cmd
