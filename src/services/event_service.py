import json
from collections import defaultdict
from typing import List

from models.event_model import Event
from models.event_model import Properties as MongoProperties
from schemas.inputs.even_input import EventsInput
from schemas.user_story_schema import StorySchema


class EventService:

    @staticmethod
    def post_events(events_input: EventsInput) -> list:
        """
        Saves a list of events to the database.

        :param events_input: An instance of EventsInput containing the events to be saved.
        :return: An instance of EventsOutput containing the saved events and a success message.
        """
        response: list = []
        for event_data in events_input.events:
            properties_dict = event_data.properties.model_dump()
            #properties_dict['elementAttributes'] = properties_dict['elementAttributes']
            properties = MongoProperties(**properties_dict)

            event = Event(
                event=event_data.event,
                properties=json.loads(properties.to_json()),
                timestamp=event_data.timestamp
            )

            event.save()
            response.append(json.loads(event.to_json()))

        return response

    @staticmethod
    def get_identified_stories_by_user(session_id: str) -> List[StorySchema]:
        """
        Retrieves user stories grouped by session ID.

        :param session_id: The session ID to filter events by. If None, retrieves all events.
        :return: An instance of StoriesOutput containing the grouped user events.
        """
        if session_id is None:
            events = Event.objects()
        else:
            events = Event.objects(properties__session_id=session_id)
        grouped_events = defaultdict(list)

        for event in events:
            event_parsed = json.loads(event.to_json())
            event_parsed["_id"] = event_parsed["_id"]["$oid"]
            session_id = event_parsed["properties"]["session_id"]
            grouped_events[session_id].append(event_parsed)

        response: list[Event] = [{"session_id": sid, "user_history": evts} for sid, evts in grouped_events.items()]

        response = [StorySchema(session_id=sid, user_history=evts) for sid, evts in grouped_events.items()]
        return response

event_service = EventService()
