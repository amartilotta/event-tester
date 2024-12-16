import os

from fastapi.templating import Jinja2Templates

from schemas.user_story_schema import UserStory

templates = Jinja2Templates(directory="/templates")

class PlaywrightTestGenerator:

    def __init__(self, output_directory="tests/generated"):
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True)

    def generate_tests(self, story: UserStory) -> str:
        """
        Generates test code from a user story.

        :param story: A dictionary containing the user story with actions.
        :return: The generated test code as a string.
        """
        test_template = templates.get_template("test_template.jinja2")

        for action in story.actions:
            if action.class_:
                selector = "." + ".".join(action.class_.split())
            else:
                selector = action.target
            action.selector = selector

        test_code: str = test_template.render(story=story.model_dump())

        return test_code

    def write_tests(self, test_to_save: str, file_name: str = "generated_tests"):
        """
        Writes the generated test code to a file.

        :param test_to_save: The test code to be saved.
        :param file_name: The name of the file to save the test code in.
        """
        output_file = os.path.join(self.output_directory, file_name + ".py")
        with open(output_file, "w") as f:
            f.write(test_to_save)

        os.chmod(output_file, 0o777)


playwright_service = PlaywrightTestGenerator()
