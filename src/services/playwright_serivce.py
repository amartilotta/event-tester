import os
from textwrap import dedent

from jinja2 import Template


class PlaywrightTestGenerator:
    def __init__(self, output_directory="tests"):
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True)

    def generate_tests(self, user_stories):
        # Template para el test
        test_template = Template(dedent(
'''
        from playwright.sync_api import sync_playwright


        {% for story in user_stories -%}
        def test_{{ story.id.split('us-')[1].replace("-","_") }}():
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()
                {% for action in story.actions -%}
                {% if action.type == '$click' -%}
                page.locator("{{ action.selector }}").click()
                {% elif action.type == '$input' -%}
                page.locator("{{ action.selector }}").fill("{{ action.selector }}", "{{ action.value }}")
                {% elif action.type == '$navigate' -%}
                page.goto("{{ action.url }}")
                {% endif -%}
                {% endfor -%}
                browser.close()

        {% endfor %}
    '''
                ))

        for story in user_stories:
            for action in story['actions']:
                if action.get("class"):
                    selector = "." + ".".join(action["class"].split())
                else:
                    selector = action.get("target")
                action['selector'] = selector


        test_code = test_template.render(user_stories=user_stories)

        output_file = os.path.join(self.output_directory, "generated_tests.py")
        with open(output_file, "w") as f:
            f.write(test_code)
playwright_service = PlaywrightTestGenerator()
