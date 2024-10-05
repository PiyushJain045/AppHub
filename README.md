# AppHub
AppHub is a Django-based platform that allows users to access multiple apps from a single page after signup and authentication. Once logged in, users can navigate to different integrated apps, each with its unique functionality. The current version includes three apps: Blog, Stock Tracker, and Frutiables (e-commerce).

# Features
- User Authentication: Secure signup/signin system to access the hub and connected apps.
- App Integration: Access multiple apps (Blog, Stock Tracker, Frutiables) through a single dashboard.
- Simple Navigation: Once authenticated, users can easily switch between apps.

# Integrated Apps:
- Blog: A simple blog platform where users can create, read, update, and delete blog posts.
- Stock Tracker: Users can track stock prices, set alerts, and get stock-related news. (Requires - Twilio API setup for SMS alerts).
- Frutiables: An e-commerce platform for buying and selling fruits and vegetables.

## Installation 
Open the folder in your preferred IDE and execute the following commands <br>
Note: **it is preferred to create a virtual environment first** <br>
- 1) pip install -r requirements.txt (Install dependencies) <br>
- 2) python manage.py migrate (setup sqlite3 db) <br>
- 3) python manage.py runserver (Run the Django development server) <br>

That's it! Access the web app at the URL provided by the Django development server (usually http://127.0.0.1:8000).
  
