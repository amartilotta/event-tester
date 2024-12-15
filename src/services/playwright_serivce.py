import os
from jinja2 import Template

class PlaywrightTestGenerator:
    def __init__(self, output_directory="tests"):
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True) 


    def generate_test(self, user_story):
        # Template para el test
        test_template = Template(
        '''
from playwright.sync_api import sync_playwright

def test_{{ story_id }}():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        {% for action in actions %}
        # {{ action.type }}
        page.locator("{{ action.selector }}").click()
        {% endfor %}
        
        browser.close()
        '''
        )

        actions = []
        for action in user_story['actions']:
            # Construir selector a partir de `class` o `target`
            if action.get("class"):
                selector = "." + ".".join(action["class"].split())  # Convertir clases en CSS selector
            else:
                selector = action.get("target", "unknown")  # Fallback al target si no hay clase

            actions.append({
                "type": action["type"],
                "selector": selector
            })

        test_code = test_template.render(
            story_id=user_story["id"].replace("-", "_"),
            actions=actions
        )

        filename = f"test_{user_story['id']}.py"
        with open(filename, "w") as f:
            f.write(test_code)
        print(f"Test generado: {filename}")
playwright_service = PlaywrightTestGenerator()