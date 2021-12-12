"""This is the app main module"""

from fastapi import FastAPI
from mangum import Mangum

from app.api.api_v1.api import api_router
from app.core.config import AppEnvironmentEnum, settings

# Swagger settings
openapi_url = f"{settings.API_V1_STR}/openapi.json"
docs_url = f"/docs-{settings.PROJECT_NAME}"

if settings.ENV_NAME == AppEnvironmentEnum.PROD.value:
    # Do not provide swagger access for production
    openapi_url = ""
    docs_url = ""


def create_app() -> FastAPI:
    """App factory"""
    app = FastAPI(title=settings.PROJECT_NAME, openapi_url=openapi_url, docs_url=docs_url)
    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.get("/")
    def root() -> dict:
        """Root endpoint for testing"""
        return {"Welcome": "to the machine"}

    return app


app = create_app()
handler = Mangum(app, log_level="warning")


def lambda_handler(event: dict, context: dict) -> Mangum:
    """Custom lambda handler"""
    return handler(event, context)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
