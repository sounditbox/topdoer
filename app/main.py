from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="Incident Tracker API")

    @app.get("/health")
    async def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()


