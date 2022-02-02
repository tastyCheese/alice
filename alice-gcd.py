def gcd(a: int, b: int) -> int:
    while b > 0:
        a %= b
        a, b = b, a
    return a


def handler(event, context):
    text = 'Назовите целые числа, и я найду их наибольший общий делитель'
    buttons = True
    if 'request' in event and not event['session']['new']:
        buttons = False
        if event['request']['command'] == 'что ты умеешь':
            text = 'Я умею находить наибольший общий у целых чисел. Просто назовите мне их, и я дам вам ответ.'
        elif event['request']['command'] == 'помощь':
            text = 'Для того, чтобы узнать наибольший общий делитель чисел, просто назовите мне их.'
        else:
            numbers = []
            correct_input = True
            for entity in event['request']['nlu']['entities']:
                if entity['type'] == 'YANDEX.NUMBER':
                    if isinstance(entity['value'], int):
                        numbers.append(entity['value'])
                    else:
                        correct_input = False
            if len(numbers) < 1:
                correct_input = False
            if correct_input:
                answer = numbers[0]
                for i in range(1, len(numbers)):
                    answer = gcd(answer, numbers[i])
                text = str(answer)
            else:
                text = 'Я умею находить наибольший общий делитель только у целых чисел.'
    response = {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': 'false'
        }
    }
    if buttons:
        response['response']['buttons'] = [
                {
                    'title': 'Помощь'
                },
                {
                    'title': 'Что ты умеешь?'
                }
            ]
    return response
