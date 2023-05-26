from app.factory import create_app

app = create_app(config_name="DEVELOPMENT")

if __name__ == "__main__":
    app.run()
