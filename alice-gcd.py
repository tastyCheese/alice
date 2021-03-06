def gcd(a: int, b: int) -> int:
    while b > 0:
        a %= b
        a, b = b, a
    return a


def handler(event, context):
    text = 'Назовите целые числа, и я найду их наибольший общий делитель.'
    if 'request' in event:
        if event['request']['command'] == 'что ты умеешь':
            text = 'Я умею находить наибольший общий делитель у целых чисел. Просто назовите мне их, и я дам вам ответ.'
        elif event['request']['command'] == 'помощь':
            text = 'Для того, чтобы узнать наибольший общий делитель чисел, просто назовите мне их.'
        else:
            numbers = []
            correct_input = True
            is_zero = False
            for entity in event['request']['nlu']['entities']:
                if entity['type'] == 'YANDEX.NUMBER':
                    if isinstance(entity['value'], int):
                        if entity['value'] == 0:
                            is_zero = True
                            correct_input = False
                        else:
                            numbers.append(entity['value'])
                    else:
                        correct_input = False
            if len(numbers) < 1:
                correct_input = False
            if correct_input:
                answer = abs(numbers[0])
                for i in range(1, len(numbers)):
                    answer = gcd(answer, abs(numbers[i]))
                text = str(answer)
            elif is_zero:
                text = 'К сожалению, ни одно число не имеет наибольшего общего делителя с нулём.'
            elif not event['session']['new']:
                text = 'Я умею находить наибольший общий делитель только у целых чисел.'
    response = {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': 'false'
        }
    }
    if event['session']['new']:
        response['response']['buttons'] = [
                {
                    'title': 'Помощь'
                },
                {
                    'title': 'Что ты умеешь?'
                }
            ]
    return response
