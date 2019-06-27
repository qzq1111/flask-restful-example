from app.factory import create_app, celery_app

app = create_app(config_name="DEVELOPMENT")
app.app_context().push()

if __name__ == "__main__":
    app.run()
