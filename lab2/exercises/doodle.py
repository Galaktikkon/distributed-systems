from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict
from threading import Lock


class Option(BaseModel):
    vote_count: int
    description: str


class Poll(BaseModel):
    question: str
    options: Dict[str, Option]


polls: Dict[str, Poll] = {}
poll_id_counter = 0
lock = Lock()

app = FastAPI()


@app.post("/poll")
async def create_poll(poll: Poll):
    global poll_id_counter
    with lock:
        poll_id = str(poll_id_counter)
        poll_id_counter += 1

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


@app.post("/poll/{id}/vote/")
async def create_vote(id: str, option: Option):
    if id not in polls:
        return JSONResponse({"error": "Poll not found"}, status_code=404)
    poll = polls[id]

    new_id = str(len(polls[id].options.keys()) + 1)

    poll.options[new_id] = option

    options_dict = {
        option_id: option.model_dump()
        for option_id, option in polls[id].options.items()
    }

    return JSONResponse(
        {
            "message": f"New option for Poll {id} created successfully",
            "options": options_dict,
        },
        status_code=200,
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
async def update_vote(id: str, option_id: str):
    if id not in polls or option_id not in polls[id].options:
        return JSONResponse({"error": "Poll or option not found"}, status_code=404)

    polls[id].options[option_id].vote_count += 1
    return JSONResponse(
        {
            "message": f"Vote updated for option {option_id} in Poll {id}",
            "vote_count": polls[id].options[option_id].vote_count,
        },
        status_code=200,
    )


@app.delete("/poll/{id}/vote/{option_id}")
async def delete_vote(id: str, option_id: str):
    if id not in polls or option_id not in polls[id].options:
        return JSONResponse({"error": "Poll or option not found"}, status_code=404)

    if polls[id].options[option_id].vote_count > 0:
        polls[id].options[option_id].vote_count -= 1
    else:
        return JSONResponse(
            {"error": "Option vote count cannot be a negative value"}, status_code=404
        )

    return JSONResponse(
        {
            "message": f"Vote updated for option {option_id} in Poll {id}",
            "vote_count": polls[id].options[option_id].vote_count,
        },
        status_code=200,
    )
