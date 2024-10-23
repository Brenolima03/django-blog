# Start a new Django project inside the current directory
django-admin startproject project .

# Start a new Django app named 'blog' inside the project
docker-compose run --rm django-app python manage.py startapp blog

# Build and start containers in the foreground
docker-compose up --build

# Run containers in detached mode
docker-compose up -d

# Run a one-time command in the Django app container (to check Python version)
docker-compose run --rm django-app python --version

# Make migrations for the Django app
docker-compose run --rm django-app makemigrations.sh

# Apply the migrations to the database
docker-compose run --rm django-app migrate.sh

# Run the Django development server
docker-compose run --rm django-app runserver.sh

# Collect static files for the project (for deployment purposes)
docker-compose run --rm django-app collectstatic.sh

# Create a Django superuser
docker-compose run --rm django-app python manage.py createsuperuser

# Enter the running Django app container's shell
docker exec -it django-app /bin/sh
