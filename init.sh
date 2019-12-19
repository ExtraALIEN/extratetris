sudo unlink /etc/nginx/sites-enabled/nginx.conf
sudo ln -s /home/extraalien/projects/extratetris/etc/nginx.conf /etc/nginx/sites-enabled
sudo service nginx stop
sudo service nginx start
killall gunicorn
killall daphne
cd tetris
gunicorn -c ../etc/gconf.py tetris.wsgi &
daphne -b 0.0.0.0 -p 9000 tetris.asgi:application
cd ..
