import logging

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from acc_server_mgr.controllers import (
    users, auth, server_config, configuration, event,
)


async def handle_http_exception(request: Request, exc: HTTPException):
    return JSONResponse(
        {
            "detail": exc.detail
        },
        status_code=exc.status_code
    )


async def handle_exception(request: Request, exc: Exception):
    return JSONResponse(
        {"status": "error", "message": str(exc)},
        status_code=500
    )

exception_handlers = {
    HTTPException: handle_http_exception,
    Exception: handle_exception
}


app = FastAPI(
    exception_handlers=exception_handlers
)
app.add_middleware(
    CORSMiddleware,
    expose_headers=[
        "Authorization",
        "Content-Type",
        "Content-Length"
        "Accept"
    ],
    allow_origins=[
        "localhost",
        "http://localhost",
        "https://localhost",
        "localhost:8081",
        "http://localhost:8081",
        "https://localhost:8081",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "Content-Length"
        "Accept"
    ]
)
app.include_router(auth.router)
app.include_router(configuration.router)
app.include_router(event.router)
app.include_router(server_config.router)
app.include_router(users.router)


if __name__ == "__main__":
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "logging.Formatter",
                "fmt": "%(name)s: %(message)s",
            }
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout"
            }
        },
        "loggers": {
            "": {
                "handlers": ["stdout"],
                "level": "DEBUG",
            }
        }
    }

    import uvicorn
    uvicorn.run(
        "acc_server_mgr.main:app",
        ssl_keyfile="../localhost+2-key.pem",
        ssl_certfile="../localhost+2.pem",
        log_config=logging_config
    )