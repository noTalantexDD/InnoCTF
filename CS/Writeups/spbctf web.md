Базовые приёмы веба

curl
	-X - метод
	-H - заголовок
	-d - тело запроса
	-o - сохранение скачиваемого файла  

easy lvl4:
curl https://example.com -o flag 
curl -d "key1=value1&key2=value2" https://example.com
curl -d '{"key1":"value1", "key2":"value2"}' -H "Content-Type: application/json" https://example.com

curl -d "want_flag=YES&code=1337" http://kslweb1.spb.ctf.su/first/level4/ 
Done! Flag: KSL{a6354c29e728214e69c8fda2298b35fb}

easy lvl5:
url encode (all special chars) -> curl -d "fun=Kaspersky%20%26%20Summer%20%26%20Lab" http://kslweb1.spb.ctf.su/first/level5/ -> 
Done! Flag: KSL{72772dd0eee640322a3ecfb24ecab17b}

easy lvl6:
curl -H "SPbCTF: Pretty cool" http://kslweb1.spb.ctf.su/first/level6/ -> 
Done! Flag: KSL{6641c847f3479f95fcd8b837b4491f32}

easy lvl7:
```python
import requests

cookies_dict = {}

for i in range(100):
    cookies_dict[f"cookies{i}"] = f"{i}"

response = requests.get("http://kslweb1.spb.ctf.su/first/level7/", cookies=cookies_dict)

print(response.text)
```
-> Done! Flag: KSL{d5a0bc3afdc571bab78da4f96c9965b5}

easy lvl13:
1) заглянуть в local storage
2) деобфусцировать JSFuck например через https://thanhle.io.vn/de4js/
KSL{63f07bbf55787eaedd9d37faeb4783ed}

easy lvl14:
curl http://kslweb1.spb.ctf.su/first/level14/index.php?give_flag=1 -o flag -> xdg-opem ./flag -> KSL{3991018732f98f43f1ffd0b76ae94f30}

manual lvl15:
скриптик на 1337 символов в linux
![[Pasted image 20261026224316.png]]
-> KSL{4e15221043cbd0619409f282dad76c0f}

manual lvl17:
```python
str1 = "Cookie: "
for i in range(0, 101):
    str1 += f"cookie{i}={i}; "
print(str1)
```
netcat -C kslweb1.spb.ctf.su 58080
GET /second/level17/ HTTP/1.1
Connection: close
Host: kslweb1.spb.ctf.su
из питона cookie

HTTP/1.1 200 OK
Date: Mon, 26 Oct 2026 16:09:29 GMT
Server: Apache/2.4.7 (Ubuntu)
X-Powered-By: PHP/5.5.9-1ubuntu4.29+0park1
Content-Length: 50
Connection: close
Content-Type: text/plain

Done! Flag: KSL{30d9525fd46020028a987071785b1033}

manual lvl18:
netcat -C kslweb1.spb.ctf.su 58080
POST /second/level18/ HTTP/1.1
Host: kslweb1.spb.ctf.su
Content-Type: application/x-www-form-urlencoded
Content-Length: 31
                               
makers=Kaspersky%20%26%20SPBCTF
HTTP/1.1 200 OK
Date: Mon, 26 Oct 2026 16:44:47 GMT
Server: Apache/2.4.7 (Ubuntu)
X-Powered-By: PHP/5.5.9-1ubuntu4.29+0park1
Content-Length: 50
Content-Type: text/plain

Done! Flag: KSL{75c8c25412af41a055b8e749858d43b2}

manual lvl21:
<form method='POST' enctype='multipart/form-data'>

