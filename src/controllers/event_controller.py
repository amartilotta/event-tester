from typing import List, Optional

from fastapi import APIRouter, HTTPException

from schemas.inputs.even_input import EventsInput
from schemas.outputs.event_output import EventsOutput
from schemas.outputs.grouped_output import GroupedOutput
from schemas.outputs.patterns_output import PatternsOutput
from schemas.outputs.stories_output import StoriesOutput
from schemas.outputs.test_output import TestOutput
from schemas.user_story_schema import Pattern, StorySchema, UserStory
from services.event_service import event_service
from services.playwright_service import playwright_service
from services.user_history_service import user_story_service

router = APIRouter()


@router.post("/event", response_model=EventsOutput)
async def post_events(events_input: EventsInput)-> EventsOutput:
    try:
        events: list = event_service.post_events(events_input)
        return EventsOutput(events=events, message="Events saved successfully.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/stories", response_model=StoriesOutput)
async def get_stories(session_id: Optional[str]=None)    :
    try:
        stories: List[StorySchema] = event_service.get_identified_stories_by_user(session_id)
        return StoriesOutput(stories=stories, message="Stories retrieved successfully.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/test", response_model=TestOutput)
async def get_test(session_id: Optional[str]=None)-> TestOutput:
    response = []
    try:
        user_stories: List[UserStory] = user_story_service.generate_users_stories()

        if session_id:
            user_stories = [
                story for story in user_stories if story.id == session_id
            ]

        for story in user_stories:
            test_generated: str = playwright_service.generate_tests(story)
            response.append({story.id: test_generated})
            #playwright_service.write_tests(test_generated, story["id"])

        return TestOutput(tests=response, message="Tests generated successfully.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/grouped-events", response_model=GroupedOutput)
async def get_grouped_events()-> GroupedOutput:
    try:
        user_stories: List[UserStory] = user_story_service.generate_users_stories()
        return GroupedOutput(users_stories=user_stories, message="Grouped events retrieved successfully.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/patterns", response_model=PatternsOutput)
async def get_patterns()-> PatternsOutput:
    try:
        patterns: List[Pattern] = user_story_service.extract_patterns()
        return PatternsOutput(patterns=patterns, message="Patterns extracted successfully.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
