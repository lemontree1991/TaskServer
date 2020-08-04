cd ..
celery multi start 1 -A TaskServer -c4  --logfile=log/celery/%p.log --pidfile=pids/celery/%p.pid