import openai
import re

openai.api_key = "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"
# model_engine = "gpt-3.5-turbo"
model_engine = 'text-davinci-003'
text = 'ху'
letters = list(text)
context = 'Паша купил большую'
# prompt = 'Я тебе подаю слово: "добрый". Выдай мне 3 самых частых в использовании предложения, которые начинаются с этого слова и вставь их в фигурные скобки ({}). Кроме этих предложений ничего не пиши'
prompt = f'Вот предложение "{context}" по контексту которого ты должен подбирать слова. ' \
         f'Я тебе подаю две буквы: "{text}". Выдай мне 9 слов, у которых первая буква "{letters[0]}",' \
         f' а вторая "{letters[1]}" и вставь их в фигурные скобки ({{}}). Кроме этих слов ничего не пиши'

# prompt = f'Я тебе подаю предложение: "{sentence}". Выдай мне 9 самых подходящих по контексту слов для продожения этого предложения. ' \
#          f'и вставь их в фигурные скобки ({{}}). Кроме этих слов ничего не пиши'
completion = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=256, n=1, stop=None,
                                      temperature=0.7)
# completion = openai.ChatCompletion.create(
#     model=model_engine,
#     messages=[
#         # {"role": "system", "content" : "You are ChatGPT, a large language model trained by OpenAI. "
#         #                                "Answer as concisely as possible.\nKnowledge cutoff: 2021-09-01\nCurrent date: 2023-03-02"},
#         {"role": "user", "content": f"{prompt}"}],
#     # max_tokens=256, n=1, stop=None, temperature=0.7)
# )
# message = completion.choices[0].message.content
message = completion.choices[0].text
print(message)
pattern = r"\{([^{}]+)\}"
matches = re.findall(pattern, message)
print(matches)
