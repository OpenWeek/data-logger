export ROOT=$(pwd)
lighttpd -f wsgi_server/lighttpd.conf -D &
