import openai
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)


def prompt_domain_expert(question):
    print(question)
    input_valid = False
    while not input_valid:
        ruling = input("Please answer with either 'y' or 'n':\n")
        if ruling == 'y':
            return True
        elif ruling == 'n':
            return False
        else:
            continue


class DefaultConversationalHandler:
    def __init__(self):
        self.client = openai.OpenAI()

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(100))
    def get_response(self, messages):
        response = openai.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=messages,
            temperature=0,
            stop=None
        ).choices[0].text.strip()
        return response

    def api_query(self, prompt, content):
        complete_prompt = prompt['content'] + '\n' + content

        reply = self.get_response(complete_prompt)
        return reply


def match(handler, comparison, prompt, lock, expert_question=f'Domain expert, please determine whether the following are similar:\n'):
    try:
        response = handler.api_query(prompt, comparison)
        if response.lower() == "yes":
            return True
        elif response.lower() == "no":
            return False
        elif response.lower() == "unsure":
            with lock:
                return prompt_domain_expert(expert_question + comparison)
        else:
            return False
    except ValueError as e:
        print(e)
