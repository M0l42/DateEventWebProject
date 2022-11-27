from fastapi import FastAPI
from EventStore.event_store import DatetimeEventStore
from .config import JSON_PATH
import json
import os

app = FastAPI()

with open(JSON_PATH, 'r') as json_read:
    event_store = DatetimeEventStore(json.load(json_read))


def commit():
    with open(JSON_PATH, 'w') as json_write:
        json.dump(event_store.events, json_write, indent=4, default=str)


@app.get("/", tags=['ROOT'])
async def root():
    return {"message": "Hello World"}


@app.get("/events", tags=['EVENTS'])
async def get_all_events():
    return {"data": event_store.events}


@app.get("/events/{start}_{end}", tags=['EVENTS'])
async def get_events(start, end):
    return {"data": event_store.get_events(start, end)}


@app.post('/events', tags=['EVENTS'])
async def add_events(event: dict):
    event_store.store_event(event['date'], event['event'])
    commit()
    return {"data": "An event has been added !"}


@app.put('/events/{id}', tags=['EVENTS'])
async def update_events(id:int, body: dict):
    event_store.update_event(id, body)
    commit()
    return {"data": "An event has been added !"}


@app.delete("/events/{id}", tags=['EVENTS'])
async def delete_event(id: int):
    event_store.delete_event([event_store.events[id]])
    commit()
    return {"data": f"events with id {id} has been deleted"}


@app.delete("/events/multi/{start}_{end}", tags=['EVENTS'])
async def delete_multiple_event(start, end):
    res = event_store.get_events(start, end)
    event_store.delete_event(res)
    commit()
    return {"data": f"events with id {id} has been deleted"}
