def gcd(a: int, b: int) -> int:
    while b > 0:
        a %= b
        a, b = b, a
    return a


def handler(event, context):
    text = 'Назовите целые числа, и я найду их наибольший общий делитель'
    if 'request' in event and 'nlu' in event['request'] and \
            'entities' in event['request']['nlu']:
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
            text = 'Запрос должен содержать только целые числа.'
    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': 'false'
        },
    }
