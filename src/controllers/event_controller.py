
from typing import Optional

from fastapi import APIRouter, HTTPException

from schemas.inputs.even_input import EventsInput
from services.event_service import event_service
from services.playwright_serivce import playwright_service
from services.user_history_service import user_story_service

router = APIRouter()


@router.post("/event")
async def post_events(events_input: EventsInput)    :#debe ser async?
    try:
        return event_service.post_events(events_input)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/stories")
async def get_stories(session_id: Optional[str]=None)    :
    try:
        return event_service.get_stories(session_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/test")
async def get_test():
    try:
        playwright_service.generate_tests(
            [
                {
                    "id": "us-56676925-6e55-4072-98db-ca544bd3dbb5",
                    "title": "User Story for 56676925-6e55-4072-98db-ca544bd3dbb5",
                    "actions": [
                        {
                            "type": "$click",
                            "class": "flex items-center justify-between",
                            "target": "div"
                        },
                        {
                            "type": "$click",
                            "class": "flex w-full h-full items-center transition-transfo...",
                            "target": "span"
                        },
                        {
                            "type": "$click",
                            "class": "flex w-full items-center rounded-md border-transpa...",
                            "target": "a"
                        }
                    ]
                },
                {
                    "id": "us-56676925-6e55-4072-98db-ca544bd3dff5",
                    "title": "User Story for 56676925-6e55-4072-98db-ca544bd3dbb5",
                    "actions": [
                        {
                            "type": "$click",
                            "class": "flex items-center justify-between",
                            "target": "div"
                        },
                        {
                            "type": "$input",
                            "class": "h-4",
                            "target": "svg",
                            "value": "LOREM"
                        },
                        {
                            "type": "$click",
                            "class": "flex w-full items-center rounded-md border-transpa...",
                            "target": "a"
                        }
                    ]
                }
            ]
        )
        return {}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/history")
async def get_history(events: dict)    :
    try:

        eventos = user_story_service.group_events_by_user(events)
        return user_story_service.generate_user_story(eventos)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/patterns")
def get_patterns(events: dict):
    try:
        #events_data = [event.dict() for event in events]
        grouped_events = user_story_service.group_events_by_user(events)
        patterns = user_story_service.extract_patterns(grouped_events)
        return {"patterns": patterns}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))