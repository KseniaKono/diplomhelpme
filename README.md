# diplomhelpme
aaaaaaaaaa

добавить в профиль просмотр оставленных комментов 
просмотр лайкнутых произведений

добавить возможность поиска

добавить рекомендации идея где юзеру предлагается оценить произведение по 5 паарметрам потом 
еще анализируются лайкнутые юзером книги и на основе этого ищутся совпадения и ему высвечивается рекомендация

добавить фоловеров

фильтрацию произведений по оценкам дате создания и комментам или типа того

сделать так чтобы нажатая кнопка меню либо убиралась либо подсвечивалась

переписать форму добавления произведения

добавить возможность посмотреть старые результаты проверки

добавить график со статистикой просмотров

вариант на случай если пойду к техподам

import http.client
import json

def check_text(request):
    if request.method == 'POST':
        api_key = 'd69477e9e12f2b481ce8ae3e3ceb3a94'
        text = request.POST['text']

        # Проверка орфографии и оригинальности
        headers = {'Content-type': 'application/json'}
        payload = {
            'text': text,
            'userkey': api_key,
            'jsonvisible': 'detail',
            'text_unique': 'float',
            'visible': 'vis_on',

        }
        conn = http.client.HTTPSConnection('api.text.ru')
        conn.request('POST', '/post', json.dumps(payload), headers)
        response = conn.getresponse()

        if response.status != 200:
            return render(request, 'error.html')

        result = json.loads(response.read().decode('utf-8'))
        print(result)
        text_uid = result['text_uid']
        uniqueness = result.get('unique', 0)

        conn.close()
        return render(request, 'result.html', {'text_uid': text_uid, 'uniqueness': uniqueness})

    return render(request, 'check_text.html')

