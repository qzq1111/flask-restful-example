from app import factory

app = factory.create_app(config_name="DEVELOPMENT")

if __name__ == "__main__":
    app.run()
