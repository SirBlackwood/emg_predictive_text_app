import openai
import re

openai.api_key="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"
model_engine='text-davinci-003'


def predict_text(two_letters, context=None, word_num=0):
    if not context:
        prompt = f'Я подаю тебе две буквы: "{two_letters}". Выдай мне 9 самых частых в использовании слов, ' \
               f'у которых первая буква "{two_letters[0]}", а вторая "{two_letters[1]}" и ' \
               f'вставь каждое слово в фигурные скобки "{{}}". ' \
               f'Кроме этих слов ничего не пиши.'
    else:
        print('мы в контексте')
        # prompt = f'Вот предложение "{context}" по контексту которого ты должен подбирать слова. ' \
        #        f'Я тебе подаю две буквы: "{two_letters}". Выдай мне 9 слов, у которых первая буква "{two_letters[0]}",' \
        #        f' а вторая "{two_letters[1]}" и вставь каждое слово в фигурные скобки ({{}}). Кроме этих слов ничего не пиши'
        # prompt = f'Продолжи по контексту предложение "{context}". Начни с букв "{two_letters}" и выдай мне 9 слов, ' \
        #          f'у которых первая буква "{two_letters[0]}", а вторая "{two_letters[1]}". Не забывай про согласование ' \
        #          f'слов русского языка – падежные окончания должны быть согласованы. Вставь каждое слово ' \
        #          f'в фигурные скобки ({{}}). Кроме этих слов ничего не пиши'
        prompt = f'Вот начало предложения "{context}". Как бы ты продолжил его, если следующее слово начинается с "{two_letters}" (это слово не должно повторяться в предложениях). ' \
                 f'Выведи девять вариантов этого предложения целиком и возьми их в фигурные скобки ({{}}). Кроме этих предложений больше ничего не пиши и не используй знаки препинания'
    completion = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=1024, n=1, stop=None,
                                        temperature=0.7)
    message = completion.choices[0].text
    print(message)
    pattern = r"\{([^{}]+)\}"
    if not context:
        return re.findall(pattern, message)
    else:
        messages = re.findall(pattern, message)
        print(messages)
        words = []
        for m in messages:
            words.append(re.sub(r'[^\w\s]', '', m).split()[word_num])
        return words





# print(predict_text("са"))
# print(predict_text("бе", "машина", 1))
# split_edit_text = ['дома', 'дорога', 'доносить', 'должен', 'достаточно', 'доступный', 'доход', 'доступ', 'дождь']
# context = ' '.join(map(str, split_edit_text[:len(split_edit_text) - 1]))
# print(context)

