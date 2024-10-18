# Start a new Django project inside the current directory
django-admin startproject project .

# Build and start containers in the foreground
docker-compose up --build

# Run containers in detached mode
docker-compose up -d

# Run a one-time command in the Django app container (to check Python version)
docker-compose run --rm django-app python --version

# Make migrations for the Django app
docker-compose run --rm django-app python manage.py makemigrations

# Apply the migrations to the database
docker-compose run --rm django-app python manage.py migrate

# Create a Django superuser
docker-compose run --rm django-app python manage.py createsuperuser

# Run the Django development server
docker-compose run --rm django-app python manage.py runserver

# Collect static files for the project (for deployment purposes)
docker-compose run --rm django-app python manage.py collectstatic

# Enter the running Django app container's shell
docker exec -it django-app /bin/sh
