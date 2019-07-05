apk add py3-psycopg2
apk add postgresql

cp postgresql.conf /etc/postgresql/
chown -R postgres:postgres /etc/postgresql/

echo "now run postgre.sh as the postgres user : su postgres"
