set FLASK_APP=app.py
set FLASK_ENV=development
set APP_SETTINGS=config.DevelopmentConfig
set DATABASE_URL=sqlite:///posts.db

flask run --host=0.0.0.0
