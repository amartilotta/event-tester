from collections import defaultdict
from datetime import datetime
from typing import Dict, List

from models.event_model import Event
from schemas.event_schema import EventSchema
from schemas.user_story_schema import Action, Pattern, UserStory


class UserStoryService:

    def _group_events_by_user(self)-> Dict[str, List[EventSchema]]:
        """
        Groups events by user (`distinct_id`) and sorts them by timestamp.

        :return: A dictionary where the keys are user IDs and the values are lists of events.
        """
        events = Event.objects()

        grouped = defaultdict(list)
        for event in events:
            try:
                event_dict = event.to_mongo().to_dict()
                distinct_id = event_dict['properties']['distinct_id']
                timestamp = event_dict['properties']['timestamp']
                event_dict['properties']['timestamp'] = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                grouped[distinct_id].append(event_dict)
            except KeyError:
                print(f"Evento inválido: {event_dict}")

        for user_id in grouped:
            grouped[user_id].sort(key=lambda x: x['properties']['timestamp'])
        return grouped

    def generate_users_stories(self) -> List[UserStory]:
        """
        Generates user stories from grouped events.

        :return: A list of user stories.
        """
        grouped_events: Dict[str, List[EventSchema]] = self._group_events_by_user()
        user_stories: List[UserStory] = []
        for user_id, events in grouped_events.items():
            actions:List[Action] = self._extract_actions_from_events(events)

            story = UserStory(
            id=user_id,
            title=f"User Story for {user_id}",
            actions=actions
        )
            user_stories.append(story)
        return user_stories

    def extract_patterns(self)-> List[Pattern]:
        """
        Extracts common patterns in user stories.

        :return: A list of patterns with their counts.
        """
        grouped_events = self._group_events_by_user()
        patterns = defaultdict(int)
        for user_id, events in grouped_events.items():
            story = [event['event'] for event in events]
            for i in range(len(story) - 1):
                pattern = f"{story[i]} -> {story[i + 1]}"
                patterns[pattern] += 1
        return [Pattern(pattern=key, count=value) for key, value in patterns.items()]

    def _extract_actions_from_events(self, events)-> List[Action]:
        """
        Converts events into actions with type, class, and value.

        :param events: A list of events to be converted into actions.
        :return: A list of actions.
        """
        actions = []
        for event in events:
            properties = event.get("properties", {})
            action = {"type": event["event"]}

            if event["event"] == "$click":
                action.update({
                    "class_": properties.get("elementAttributes", {}).get("class"),
                    "target": properties.get("elementType")
                })
            elif event["event"] == "$input":
                action.update({
                    "class_": properties.get("elementAttributes", {}).get("class"),
                    "target": properties.get("elementType"),
                    "value": properties.get("elementText")
                })
            elif event["event"] == "$navigate":
                action.update({
                    "target": properties.get("elementType"),
                    "url": properties.get("current_url")
                })

            actions.append(action)
        return actions


user_story_service = UserStoryService()
