from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Literal
from threading import Lock
from uuid import uuid4


def generate_unique_id(existing_ids: set) -> str:
    while True:
        new_id = str(uuid4())
        if new_id not in existing_ids:
            return new_id


class Option(BaseModel):
    vote_count: int
    description: str


class Poll(BaseModel):
    question: str
    options: Dict[str, Option]


polls: Dict[str, Poll] = {}
UpdateOption = Literal["add", "remove"]


lock = Lock()

app = FastAPI()


@app.post("/poll")
async def create_poll(poll: Poll):
    poll_id = generate_unique_id(set(polls.keys()))
    polls[poll_id] = poll
    return JSONResponse(
        {
            "message": "Poll created successfully",
            "poll_id": poll_id,
            "poll": poll.model_dump(),
        },
        status_code=201,
    )


@app.get("/poll/{id}")
async def read_poll(id: str):
    if id not in polls:
        return JSONResponse({"error": "Poll not found"}, status_code=404)
    return JSONResponse(
        {"message": "Poll retrieved successfully", "poll": polls[id].model_dump()},
        status_code=200,
    )


@app.put("/poll/{id}")
async def update_poll(id: str, poll: Poll):
    if id not in polls:
        return JSONResponse({"error": "Poll not found"}, status_code=404)
    polls[id] = poll
    return JSONResponse(
        {"message": "Poll updated successfully", "poll": poll.model_dump()},
        status_code=200,
    )


@app.delete("/poll/{id}")
async def delete_poll(id: str):
    if id not in polls:
        return JSONResponse({"error": "Poll not found"}, status_code=404)
    del polls[id]
    return JSONResponse({"message": "Poll deleted successfully"}, status_code=200)


@app.get("/poll/{id}/vote")
async def read_votes(id: str):
    if id not in polls:
        return JSONResponse({"error": "Poll not found"}, status_code=404)

    options_dict = {
        option_id: option.model_dump()
        for option_id, option in polls[id].options.items()
    }

    return JSONResponse(
        {
            "message": f"Poll {id} options retrieved successfully",
            "options": options_dict,
        },
        status_code=200,
    )


@app.post("/poll/{poll_id}/vote")
async def create_vote(poll_id: str, option: Option):
    if poll_id not in polls:
        return JSONResponse({"error": "Poll not found"}, status_code=404)

    option_id = generate_unique_id(set(polls[poll_id].options.keys()))
    polls[poll_id].options[option_id] = option

    return JSONResponse(
        {
            "message": f"New option added to Poll {poll_id}",
            "option_id": option_id,
            "option": option.model_dump(),
        },
        status_code=201,
    )


@app.get("/poll/{id}/vote/{option_id}")
async def read_vote(id: str, option_id: str):
    if id not in polls or option_id not in polls[id].options:
        return JSONResponse({"error": "Poll or option not found"}, status_code=404)

    return JSONResponse(
        {
            "message": f"Poll {id} option {option_id} retrieved successfully",
            "option": {
                "option_id": option_id,
                "vote_count": polls[id].options[option_id].vote_count,
            },
        },
        status_code=200,
    )


@app.put("/poll/{id}/vote/{option_id}")
async def update_vote(id: str, option_id: str, update_option: UpdateOption):
    if id not in polls or option_id not in polls[id].options:
        return JSONResponse({"error": "Poll or option not found"}, status_code=404)

    if update_option == "add":
        polls[id].options[option_id].vote_count += 1
    elif update_option == "remove":
        if polls[id].options[option_id].vote_count > 0:
            polls[id].options[option_id].vote_count -= 1
        else:
            return JSONResponse(
                {"error": "Option vote count cannot be negative"}, status_code=400
            )
    else:
        return JSONResponse({"error": "Incorrect update option"}, status_code=400)

    return JSONResponse(
        {
            "message": f"Vote {update_option}ed for option {option_id} in Poll {id}",
            "vote_count": polls[id].options[option_id].vote_count,
        },
        status_code=200,
    )


@app.delete("/poll/{id}/vote/{option_id}")
async def delete_vote(id: str, option_id: str):
    if id not in polls or option_id not in polls[id].options:
        return JSONResponse({"error": "Poll or option not found"}, status_code=404)

    del polls[id].options[option_id]

    return JSONResponse(
        {"message": f"Option {option_id} deleted from Poll {id}"},
        status_code=200,
    )
