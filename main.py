import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.db.database import init_db


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hellow world!"

def create_app():
    schema = strawberry.Schema(Query)
    qraphql_app = GraphQLRouter(schema)
    app = FastAPI()

    app.include_router(qraphql_app, prefix="/graphql")
    return app

app = create_app()

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def ping():
    return {"ping": "pong"}
