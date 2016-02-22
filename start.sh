echo 'Starting server'
nohup ~/.local/bin/gunicorn index:index -w 4 -b 0.0.0.0:8080 & > log
echo 'Success'