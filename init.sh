sudo unlink /etc/nginx/sites-enabled/nginx.conf
sudo ln -s /home/extraalien/projects/extratetris/etc/nginx.conf /etc/nginx/sites-enabled
sudo service nginx stop
sudo service nginx start
killall gunicorn
gunicorn -c etc/gconf.py testapp:app
