bandit0:
ssh -> ls -> cat -> 6y2kwnwK6grgvwvpvLaa2T1cpFEKOhNR -> exit

bandit1:
cat ./- -> PK8fYLZg2hnHSz83plBL1iEPKdD3QToB

bandit2:
cat ./--Tab / cat./"--spaces in the filename--" -> 7ZZ2LFrykP2zEyvBl4m3clcL7tGYJPME

bandit3:
cd -> ls -la -> xzTXq1rDJQVVAzdv5cHq1TQytTWufAMq

bandit4:
file ./* -> ASCII -> 6C7h9GD8M6ai5nr7wo1RonrzFjj9yIrG

bandit5:
find -size 1033c -> pXa26xhMWaC2SvDotA4r9EgZkulOeSBW

bandit6:
find / -user bandit7 -group bandit6 -size 33c 2>/dev/null -> Bmnnvf82KzQlfxgAI2d1zYbr1u9pr3E3

bandit7:
man grep -> grep millionth data.txt -> VR1ljMayciFxbnUokuQmJFw6QC9VKtub

bandit8:
sort data.txt | uniq -u -> EjmOSvuAu7sGAHqHVcBDPirRe9T03kxl

bandit9:
strings data.txt | grep "=" -> B0s2khmbT9u0geKuOoVGW3JZKhndE3BG

bandit10:
base64 -d data.txt -> pYfOY6HwUsDj5rL9UvyhU7MCmv8vN5Ro

bandit11:
cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m' -> GROozWPO8QyN0mGrjUkID0WCYkZiQxrN

bandit12:
xxd -r data.txt > data1.txt -> кучу проверок через file, добавлений суффикса .bz2/.gz, кучу распаковок gzip -d/bzip2 -d/tar -xf -> qQYQiHOBPR8zR61qxYqX45quvihF2uzk 

bandit13:
exit -> chmod o-rwx sshkey.private, chmod g-rwx sshkey.private-> ssh -i /home/sshkey.private bandit14@bandit.labs.overthewire.org -p 2220

bandit14:
nc/ncat localhost 30000 < /etc/bandit_pass/bandit14 -> pbLYuZtTg4MgaqfJx8jbA9gKKGqM68A7 (netcat/ncat передаёт через tcp или udp данные на сервер)

bandit15:
ncat --ssl localhost 30001 -> kS0Hf0u5HiXFwKMKFqXvPdOTNGGa0X8V

bandit16:
nmap -p 31000-32000 localhost -> 
31046/tcp open  unknown
31518/tcp open  unknown
31691/tcp open  unknown
31790/tcp open  unknown
31960/tcp open  unknown -> сканируем все через nmap c флагом -sV и видим что все кроме 31790 отправляют echo или ssl/echo -> nmap -sV -p 31790 localhost -> 31790/tcp open  ssl/unknown -> ncat --ssl localhost 31790 -> получаем ssh ключ -> формируем ключ как в задании 13

bandit17:
diff -y passwords.old passwords.new / без флага -> OQxXZjELndr90zuhOTDYBEomI0SZITXI

bandit18:
ssh -t bandit18@bandit.labs.overthewire.org -p 2220 "bash --norc" / ssh bandit18@bandit.labs.overthewire.org -p 2220 "bash" / scp   -> cat readme -> KpsOfPkcP7i1FlIExk2QEjyt6dw8dxZI

--norc - «no Run Commands»_. Когда вы используете эту команду, Bash игнорирует системный файл `/etc/bash.bashrc` и ваш личный файл настроек `~/.bashrc`.
-t - **принудительно выделяет псевдотерминал (pseudo-terminal, или tty)** на удаленном сервере. Eсли вы передаете в SSH конкретную команду для выполнения (например, `ssh user@host "команда"`), SSH запускает её в неинтерактивном режиме **без выделения терминала**

scp -P 2220 bandit18@bandit.labs.overthewire.org:~/readme ~/Desktop/

bandit19:
./bandit20-do -> 
Run a command as another user.
  Example: ./bandit20-do whoami

./bandit20-do cat /etc/bandit_pass/bandit20 -> 4pIjcunZ0fK2vmp3IwfG8Vf7VhxD6pOA

bandit20:
в двух терминалах запускам ncat в режиме прослушивания и suconnect
режим прослушивания - состояние сетевой программы, при котором она **ожидает входящие запросы** от других устройств (клиентов) на определенном сетевом порту

1st term) echo "4pIjcunZ0fK2vmp3IwfG8Vf7VhxD6pOA" | ncat -l 1234 <- отправит текст первому кто подключится к порту
2nd term) ./suconnect 1234 <- подключается к порту 1234, проверяет что отправили через ncat, отправляет обратно пароль 

bW9kBv5WC3P4yoDyf12LSdGuNz5ka6hY

bandit21:
cd /etc/cron.d/ -> cat cronjob_bandit22 (смотрим программу которая выполняется) -> cat /usr/bin/cronjob_bandit22.sh -> cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv -> cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv -> RYVux2rHEm9tiXHmLFzuR7Vhx6AZQMEz

bandit22:
cat cronjob_bandit23 -> cat /usr/bin/cronjob_bandit23.sh -> читаем программу и понимаем что она делает -> cat /etc/bandit_pass/ $myname > /tmp/ $mytarget -> если myname = bandit22, значит он копирует из bandit_pass/bandit22 который нам уже доступен, попробуем подставить bandit23 в вычислении чек-суммы и проверить папку /tmp/ -> echo I am user bandit23 | md5sum -> cat /tmp/8ca319486bfbbc3663ea0fbe81326349 ->
gKXDTAXnIz3OBxiPjRZ2uqutUlPZrBsw

bandit23:
cat /usr/bin/cronjob_bandit24.sh -> ищет все файлы в папке /var/spool/bandit24/foo и запускает их если владелец bandit23(мы), иначе удаляет -> можно подкинуть скрипт в папку:
```bash
#!/bin/bash
cat /etc/bandit_pass/bandit24 > /tmp/mymymy/my.txt
```

-> НО! нужно чтобы у bandit24(он его и будет исполнять) были права на запись в директорию и файл, а также чтение и исполнение скрипта -> chmod -R 777 /tmp/mymymy/ -> закидываем скрипт в папку, через минуту в my.txt появится пароль -> hVQMk3lJNsmQ7VF3ubyrNNBom7BOgVXv

bandit24:
brute-forcing
```bash
#!/bin/bash
for (( i = 0; i <= 9; i++ )); do
        for (( j = 0; j <= 9; j++ )); do
                for (( k = 0; k <= 9; k++ )); do
                        for (( l = 0; l <= 9; l++ )); do
                                echo "hVQMk3lJNsmQ7VF3ubyrNNBom7BOgVXv $i$j$k$l"  
                        done
                done
        done
done | ncat localhost 30002 
```
-> bash bandit24.sh -> SoHfqMOEqIX2IYKVciZxvgpR9a2Djx4P

bandit25/26:
cat /etc/passwd -> cat /usr/bin/showtext -> `more ~/text.txt` странная команда...  more переходит в интерактивный режим ожидания, только если текст не помещается на один экран (при нажатии v в режиме ожидания можно перейти в vim, а в любом текстовом редакторе линукс есть встроенное выполнение команд ) -> ssh -i /home/text.private bandit26@bandit.labs.overthewire.org -p 2220 -> переходим в режим ожидания -> :set shell=/bin/bash -> :!ls -> :!./bandit27-do cat /etc/bandit_pass/bandit27 -> STJLJBRRphMxKB392CT4iOr5CbzPU9ER

: - делает сам vin
:! - делает командная оболочка

bandit27:
git clone ssh://bandit27-git@bandit.labs.overthewire.org:2220/home/bandit27-git/repo ~/Desktop/git -> y8Yd2ssKcpHpud7UvOSOxwamRMzIGIeQ

bandit28:
git clone ssh://bandit28-git@bandit.labs.overthewire.org:2220/home/bandit28-git/repo /home/roman/Desktop/git -> 
```
Bandit Notes
Some notes for level29 of bandit.
credentials
- username: bandit29
- password: xxxxxxxxxx
```
-> git log -> git log -p -> Em7eGtqaMySwNFjCpwzzHhLhospOcdt0

bandit29:
cat readme.md ->
```
Bandit Notes
Some notes for bandit30 of bandit.
credentials
- username: bandit30
- password: <no passwords in production!>
```
-> **`.git/packed-refs`**, используется системой контроля версий **Git** для оптимизации хранения ссылок (веток и тегов) -> cat .git/packed-refs (находим что есть различные ветки) ->  git checkout dev -> git log -p -> jq9Dfg2rXsfYsWMgFuKlXhphjdH7USgX

bandit30:
cat README.md -> just an epmty file... muahaha -> cat packed-refs(находим, что есть ветка и тег) -> git tag -> git show secret -> 82NkymblpGBYmIXG6ZQ8YldBYstHpfUf

bandit31:
cat README.md ->
```
This time your task is to push a file to the remote repository.
Details:
    File name: key.txt
    Content: 'May I come in?'
    Branch: master
```
-> во первых замечаем что тут есть .gitgnore, который игнорирует наши файлы .txt, удаляем -> git add . -> git commit -m "May I come in?" -> git push -> pWuj5jBQ6IgV0NXwiH6g1pXRF8S1YvbT

bandit32:
видим оболочку которая мешает нам выполнять команды переводя их в верхний регистр. Давайте найдём команду которая не состоит из букв. Чтобы её можно было выполнить.
специальная переменная **`$0`** хранит имя или путь запущенного скрипта либо имя текущей оболочки.

$0 -> cat /etc/bandit_pass/bandit33 -> u4P2CyPOwPGLe94RdD9Uo2FxFwvnFswM

bandit33:
cat README.txt
