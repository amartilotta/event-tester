import json
from collections import defaultdict

from models.event_model import Event
from models.event_model import Properties as MongoProperties
from schemas.inputs.even_input import EventsInput
from schemas.outputs.event_output import EventsOutput
from schemas.outputs.stories_output import StoriesOutput
from playwright.sync_api import sync_playwright


class EventService:

    @staticmethod
    def post_events(events_input: EventsInput) -> EventsOutput:
        response = []
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


        return EventsOutput(
            events=response,
            message="Succefssfully saved")

    @staticmethod
    def get_stories(session_id: str) -> EventsOutput:
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

        response = [{"session_id": sid, "user_history": evts} for sid, evts in grouped_events.items()]

        return StoriesOutput(
            users_events=response,
        )

    # @staticmethod
    # def get_test(session_id: str) -> any:
    #     events = event_service.get_stories(session_id)
    #     event_service._sort_events(events)
    #     event_service._generate_test_with(events)

    #     return 1

    # def _sort_events(events):
    #     for event in events:
    #         event["events"].sort(key=lambda x: x["timestamp"])

    # def _generate_test_with_playwright(user_events):
    #     with sync_playwright() as p:
    #     # Lanzar el navegador
    #         browser = p.chromium.launch(headless=False)
    #         context = browser.new_context()
    #         page = context.new_page()

    #         for user in user_events["users_events"]:
    #             for event in user["user_history"]:
    #                 event_type = event["event"]
    #                 properties = event["properties"]

    #                 # Obtener información del evento
    #                 element_text = properties.get("elementText", "")
    #                 element_type = properties.get("elementType", "")
    #                 current_url = properties.get("current_url", "")
    #                 referrer = properties.get("referrer", "")
    #                 input_data = properties.get("elementAttributes", {}).get("value", "")

    #                 # Manejar eventos según el tipo
    #                 if event_type == "$click":
    #                     try:
    #                         # Intentar encontrar el elemento con el texto específico
    #                         page.locator(f"div:has-text('{element_text}')").click()
    #                     except Exception as e:
    #                         print(f"No se pudo hacer click en el elemento: {e}")
    #                         assert3

    #                 elif event_type == "navigation":
    #                     print(f"Navegando a: {referrer}")
    #                     try:
    #                         page.goto(referrer)
    #                     except Exception as e:
    #                         print(f"No se pudo navegar a la URL: {e}")

    #                 elif event_type == "input":
    #                     print(f"Llenando input con el valor: {input_data}")
    #                     try:
    #                         # Buscar el input según su tipo o placeholder
    #                         input_locator = page.locator(f"input[value='{input_data}']")
    #                         input_locator.fill(input_data)
    #                     except Exception as e:
    #                         print(f"No se pudo llenar el input: {e}")
    #                 else:
    #                     print(f"Tipo de evento desconocido: {event_type}")

    #     # Cerrar el navegador
    #     browser.close()


event_service = EventService()
