from collections import defaultdict
from datetime import datetime

from models.event_model import Event


class UserStoryService:
    def __init__(self):
        pass

    def group_events_by_user(self, events):
        """
        Agrupa eventos por usuario (`distinct_id`) y los ordena por timestamp.
        """
        events = Event.objects()

        grouped = defaultdict(list)
        for event in events:
            try:
                event_dict = event.to_mongo().to_dict()
                distinct_id = event_dict['properties']['distinct_id']
                timestamp = event_dict['properties']['timestamp']
                # Convertir timestamp a datetime
                event_dict['properties']['timestamp'] = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                grouped[distinct_id].append(event_dict)
            except KeyError:
                print(f"Evento inválido: {event_dict}")

        # Ordenar eventos dentro de cada usuario por timestamp
        for user_id in grouped:
            grouped[user_id].sort(key=lambda x: x['properties']['timestamp'])
        return grouped

    def generate_user_story(self, grouped_events):
        """
        Genera historias de usuario a partir de eventos agrupados.
        """
        user_stories = []
        for user_id, events in grouped_events.items():
            story_id = f"us-{user_id}"
            actions = self._extract_actions_from_events(events)

            story = {
                "id": story_id,
                "title": f"User Story for {user_id}",
                "actions": actions
            }
            user_stories.append(story)
        return user_stories

    def extract_patterns(self, grouped_events):
        """
        Extrae patrones comunes en las historias de usuario.
        """
        patterns = defaultdict(int)
        for user_id, events in grouped_events.items():
            story = [event['event'] for event in events]
            for i in range(len(story) - 1):
                pattern = f"{story[i]} -> {story[i + 1]}"
                patterns[pattern] += 1
        return patterns

    def _extract_actions_from_events(self, events):
        """
        Convierte eventos en acciones con tipo, class y valor.
        """
        actions = []
        for event in events:
            properties = event.get("properties", {})
            action = {"type": event["event"]}

            if event["event"] == "$click":
                action.update({
                    "class": properties.get("elementAttributes", {}).get("class"),
                    "target": properties.get("elementType")
                })
            elif event["event"] == "$input":
                action.update({
                    "class": properties.get("elementAttributes", {}).get("class"),
                    "target": properties.get("elementType"),
                    "value": properties.get("elementText")
                })
            elif event["event"] == "$navigate":
                action.update({
                    "target": properties.get("elementType"),
                    "url": properties.get("$current_url")
                })

            actions.append(action)
        return actions


user_story_service = UserStoryService()