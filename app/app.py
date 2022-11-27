from fastapi import FastAPI
from EventStore.event_store import DatetimeEventStore

app = FastAPI()
event_store = DatetimeEventStore()


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
async def add_events(event:dict):
    event_store.store_event(event['date'], event['event'])
    return {"data": "An event has been added !"}
