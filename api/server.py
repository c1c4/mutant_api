from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.routes import dna, statistics

def get_application():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(dna.router)
    app.include_router(statistics.router)

    return app


app = get_application()
