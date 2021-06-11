rm -rf crittercatcherapi/migrations
rm db.sqlite3
python manage.py makemigrations crittercatcherapi
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata requestors
python manage.py loaddata categories
python manage.py loaddata requests
python manage.py loaddata reviews
