curl --location --request POST 'http://94.19.79.169:20001/api/ticket/check' \
--header 'Accept: */*' \
--header 'Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7' \
--header 'Connection: keep-alive' \
--header 'Content-Length: 0' \
--header 'Content-Type: application/json' \
--header 'Origin: http://94.19.79.169:20001' \
--header 'Referer: http://94.19.79.169:20001/' \
--header 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36' \
--header 'Cookie: JSESSIONID=0A1A090B46CFD234D3390FA2D83A44D8; JSESSIONID=C68E6B3A7B76FF5AC01DA4B358AE5D96'

1st JSESSIONID - auth
2st JSESSIONID - ticket?

{
    "message": "К сожалению, билет ticket-d6e780fe проиграл."
}

C68E6B3A7B76FF5AC01DA4B358AE5D96
D6E780FE = 3605496062
md5 4d05e915af76cff5ba701083198bd2f0 31bf1d2aa0d2a87e56890951d72c7831

Polyphemus 3000
Enter hex to decrypt, or press Enter to continue.
> 00000000000000000000000000000000d6e780fe000000000000000000000000
dec: cea07063f3756657108709f773c6b962
> 00000000000000000000000000000000000000000000000000000000d6e780fe
dec: cea07063f3756657108709f773c6b962
