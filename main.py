from fastapi import FastAPI, Response, HTTPException, Cookie
from uuid import uuid4

app = FastAPI()

@app.get("/new_session")
async def new_session(response: Response):
    response.set_cookie(key="session_id", value=uuid4().hex)

    return HTTPException(status_code=201)

@app.post("/game_step")
def game_step(session_id = Cookie()):
    ...
