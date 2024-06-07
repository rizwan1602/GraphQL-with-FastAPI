import asyncio
import random
import json
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import strawberry
from strawberry.fastapi import GraphQLRouter
import redis
from igraph import Graph
from pydantic import BaseModel

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis Configuration
redis_host = "localhost"
redis_port = 6379
r = redis.Redis(host=redis_host, port=redis_port, db=0)

# Create a static graph
g = Graph()
g.add_vertices(10)
g.add_edges([(i, i + 1) for i in range(9)])

@strawberry.type
class Node:
    id: int

@strawberry.type
class Edge:
    source: int
    target: int

@strawberry.type
class RouteData:
    nodes: List[Node]
    edges: List[Edge]

@strawberry.type
class StaticData:
    route_data: RouteData

@strawberry.type
class Query:
    @strawberry.field(name="static_data")
    def static_data(self) -> StaticData:
        nodes = [Node(id=v.index) for v in g.vs]
        edges = [Edge(source=e.source, target=e.target) for e in g.es]
        return StaticData(route_data=RouteData(nodes=nodes, edges=edges))

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/v1/static_data")

# Live data model
class RobotLiveData(BaseModel):
    BatteryPercent: int
    RouteNo: int
    LatestPose: int
    IsRobotEStopPressed: bool
    IsObstacleDetected: bool
    IsLidarObstacle: bool
    IsCameraObstacle: bool
    IsUSSObstacle: bool
    IsCliffObstacle: bool
    IsOnline: bool
    AllSensorsOkay: bool
    IsCameraSensorOkay: bool
    IsLidarSensorOkay: bool
    isUSSSensorOkay: bool
    OperationMode: int  # 0: Manual, 1: Auto
    IsBatteryCharging: bool
    IsRobotMoving: bool

# Simulate live data updates
async def update_live_data():
    while True:
        live_data = []
        for robot_id in range(5):  # Simulating data for 5 robots
            robot_data = RobotLiveData(
                BatteryPercent=random.randint(0, 100),
                RouteNo=random.randint(0, 10),
                LatestPose=random.randint(0, 9),
                IsRobotEStopPressed=bool(random.getrandbits(1)),
                IsObstacleDetected=bool(random.getrandbits(1)),
                IsLidarObstacle=bool(random.getrandbits(1)),
                IsCameraObstacle=bool(random.getrandbits(1)),
                IsUSSObstacle=bool(random.getrandbits(1)),
                IsCliffObstacle=bool(random.getrandbits(1)),
                IsOnline=bool(random.getrandbits(1)),
                AllSensorsOkay=bool(random.getrandbits(1)),
                IsCameraSensorOkay=bool(random.getrandbits(1)),
                IsLidarSensorOkay=bool(random.getrandbits(1)),
                isUSSSensorOkay=bool(random.getrandbits(1)),
                OperationMode=random.choice([0, 1]),
                IsBatteryCharging=bool(random.getrandbits(1)),
                IsRobotMoving=bool(random.getrandbits(1)),
            )
            live_data.append(robot_data.dict())
        
        r.publish("robots_live_data", json.dumps(live_data))
        await asyncio.sleep(2)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(update_live_data())

@app.get("/v1/robots/live_data")
async def get_live_data():
    pubsub = r.pubsub()
    pubsub.subscribe("robots_live_data")

    while True:
        message = pubsub.get_message(ignore_subscribe_messages=True)
        if message:
            data = json.loads(message['data'])
            return data
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

