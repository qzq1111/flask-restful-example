from app.factory import create_app, celery_app

app = create_app(config_name="PRODUCTION")
app.app_context().push()
