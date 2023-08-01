import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.db.database import init_db
from app.v1.graphql_api.context import get_context
from app.v1.graphql_api.core import Mutation, Query


def create_app():
    schema = strawberry.Schema(query=Query, mutation=Mutation)
    qraphql_app = GraphQLRouter(schema, context_getter=get_context)
    app = FastAPI()

    app.include_router(qraphql_app, prefix='/graphql')
    return app


app = create_app()


@app.on_event('startup')
async def on_startup():
    await init_db()
