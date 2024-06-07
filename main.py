import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from sqlalchemy.orm import Session
from typing import List , Optional

from models import User, SessionLocal

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GraphQL types and resolvers
@strawberry.type
class UserType:
    id: int
    name: str
    age: int

@strawberry.type
class Query:
    @strawberry.field
    def user(self, info, name: Optional[str] = None, age: Optional[int] = None) -> Optional[UserType]:
        db: Session = next(get_db())
        query = db.query(User)
        
        if name is not None:
            query = query.filter(User.name == name)
        
        if age is not None:
            query = query.filter(User.age == age)
        
        return query.first()

        

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_user(self, info, name: str , age: int) -> UserType:
        db: Session = next(get_db())
        user = User(name=name, age=age)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

schema = strawberry.Schema(query=Query, mutation=Mutation)

# FastAPI setup
app = FastAPI()
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
