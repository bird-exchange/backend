from backend.app import create_app
from backend.config import config


def main():
    app = create_app()

    app.run(
        port=config.server.port,
        host=config.server.host,
        debug=False
    )
    return app


if __name__ == "__main__":
    main()
