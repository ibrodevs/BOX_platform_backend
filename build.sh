#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Create superuser (optional - if you want to create admin automatically)
# python manage.py shell -c "from accounts.models import User; User.objects.create_superuser('admin', 'admin@bivolboxing.com', 'admin123') if not User.objects.filter(username='admin').exists() else None"
