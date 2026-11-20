# ***Архитектура Linux***
### Главная схема:
Приложение → Shell → системные вызовы → ядро → железо

Kernel (ядро) — управляет CPU, RAM, процессами, устройствами, сетью, файловыми системами.
User Space — приложения, shell, службы и утилиты, работающие вне ядра.
System Call — механизм, через который программа обращается к ядру.
Shell — программа, которая интерпретирует команды (bash, zsh).
Terminal — интерфейс, через который пользователь взаимодействует с shell.
- shell не передаёт команды ядру напрямую. Shell запускает программы, а программы при необходимости используют системные вызовы.

### Основные компоненты ядра:
- Process management — процессы и планирование CPU.
- Memory management — виртуальная память и RAM.
- Device drivers — взаимодействие с устройствами.
- VFS/filesystems — работа с файлами и файловыми системами.
- Networking — сетевой стек.
### как запускается и дистрибутивы
существуют разные дистрибутивы (или «дистры»). Дистрибутив = ядро + пакетный менеджер + системные утилиты + ПО + настройки

```
BIOS/UEFI
   ↓
Bootloader (например, GRUB)
   ↓
Linux Kernel
   ↓
init/systemd (поднимает все службы и обеспечивает функционирование системы)
   ↓
службы
   ↓
login / графическая среда
```

systemd управляет множеством фоновых служб, таких как сетевые подключения, регистрация событий и SSH-сервер. Управление службами осуществляется через команду systemctl.
```bash
systemctl status ssh
systemctl start ssh
systemctl stop ssh
```

События и действия системы фиксируются в журналах, собираемых journald. Эти журналы можно просматривать с помощью команды journalctl для отслеживания ошибок и действий системы.


### ФС
важно понимать, что в Linux всё — это файл. Программы, устройства, процессы — всё может быть представлено как файл

Всё в Linux организовано в виде дерева каталогов, где корень системы — это /

/
├── home/
├── etc/
├── var/
├── usr/
├── tmp/
├── dev/
├── proc/
└── ...
Всё что мы подкючаем в фс (диски и файловые системы) подключается через mount point

VFS (Virtual file system) - абстракция ядра, позволяющая работать с разными файловыми системами через единый интерфейс. Это даёт возможность работать с данными из разных источников через единый механизм. В Linux устройства также представляют собой файлы, которые расположены в каталоге /dev. Например, диск может быть доступен как файл /dev/sda, а ваш терминал — это файл /dev/tty.

              приложения
                   ↓
                  VFS
             ↙    ↓    ↘
          ext4   XFS   Btrfs



# ***Терминал***
### FIFO
FIFO - это специальный тип файла, используемый для обмена данными между независимыми процессами (Inter-Process Communication, IPC). 
```console
mkfifo my_pipe
cat my_pipe
echo "Привет из другого процесса!" > my_pipe
```
OR
```console
cat /tmp/flag_fifo & /challenge/run > /tmp/flag_fifo
```
### stdin / stdout / stderr
У процесса стандартно есть три потока (descriptions):
FD: 0 → stdin   ввод
FD: 1 → stdout  обычный вывод
FD: 2 → stderr  ошибки
1) | - pipeline (связывает процесс с процессом в отличие от > который связывает процесс с файлом)
2) command < input.txt
перенаправляет
3) command <- многострочный документ
command << EOF
строка1
строка2
EOF
4) command <<< "text" (here-string)
тоже самое, что и `<< (но менее громоздко)` или `echo "text" | command` или `command < <(echo "text")`
5) stdout → файл
command > output.txt
Перезаписывает файл.
6) stdout → конец файла
command >> output.txt
Добавляет файл.
7) stderr → файл
command 2> error.log
8) stdout + stderr
command &> output.log
или
command >& output.log
или 
command 2>&1
Направь поток `2` (stderr) по адресу (`&`) потока `1` (stdout)
command 2>&1 | grep pwn
9) command1 2> >(command2) | command3
разделение stderr и stdout в command2 и command3
10) 
'...' — не раскрывает переменную 
"..." — раскрывает переменную
\ - экранирование
### Command/Process substitution
Результат одной команды можно вставить в другую:
$(command)
Старый вариант:
\`command\`
Лучше использовать $().

| **`<(command)`** | Подстановка процесса для **чтения** | Вывод команды внутри скобок (`stdout`) превращается в «файл», который можно **прочитать** снаружи.                  |
| ---------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **`>(command)`** | Подстановка процесса для **записи** | Внешняя команда **записывает** данные в «файл», который затем отправляется на вход (`stdin`) команды внутри скобок. |
### Условия
&&
Выполнить вторую команду только если первая успешна
||
Выполнить вторую, если первая завершилась ошибкой
;
Выполнить следующую команду независимо от результата

### утилиты
##### apt
Просмотр текущих репозиториев
Чтобы увидеть текущие репозитории, вы можете просмотреть файл sources.list:

cat /etc/apt/sources.list
Пример содержимого:

Если репозиторий требует добавления ключа для проверки подлинности, вы можете добавить его с помощью команды wget или curl и импортировать с помощью apt-key:

wget -qO - https://example.com/repo/key.gpg | sudo apt-key add
##### sed
```
sed "s/oldword/newword/g"
```

`s/` - substitute  
`oldword` - the word to replace  
`newword` - the replacement for `oldword`  
`/g` - global (search for all occurrences of the pattern)
##### tee
```console
hacker@dojo:~$ echo hi | tee pwn college
hi
hacker@dojo:~$ cat pwn
hi
hacker@dojo:~$ cat college
hi
```
OR
```console
hacker@dojo:~$ command_1 | command_2
Command 2 failed!
hacker@dojo:~$ command_1 | tee cmd1_output | command_2
Command 2 failed!
hacker@dojo:~$ cat cmd1_output
Command 1 failed: must pass --succeed!
hacker@dojo:~$ command_1 --succeed | command_2
Commands succeeded!
```
OR
```console
hacker@dojo:~$ echo HACK | tee THE > PLANET
hacker@dojo:~$ cat THE
HACK
hacker@dojo:~$ cat PLANET
HACK
hacker@dojo:~$
```
OR
```console
hacker@dojo:~$ echo HACK | tee THE | cat
HACK
hacker@dojo:~$ cat THE
HACK
hacker@dojo:~$
```
OR
```console
echo HACK | rev
KCAH
hacker@dojo:~$ echo HACK | tee >(rev)
HACK
KCAH
```

##### tr
```console
echo OWN | tr O P
PWN

#It can also handle multiple characters, with the characters in different positions of the first argument replaced with associated characters in the second argument.
echo PWM.COLLAGE | tr MA NE
PWN.COLLEGE

#также можно использовать диапазоны символов или значений
/challenge/run | tr [A-Z][a-z][1-9] [a-z][A-Z]0

#удаление символов 
tr -d A
```
заметочка:
'...' — не раскрывает переменную 
"..." — раскрывает переменную
\ - экранирование
##### head
The `head` command is used to display the first few lines of its input:
```console
#By default, it shows the first 10 lines, but you can control this with the `-n` option:

cat /something/very/long | head -n 2
this
is
```
##### cut
Sometimes, you want to grab specific columns of data, such as the first column, the third column, or the 42nd column. For this, there's the `cut` command.
```console
cat scores.txt
hacker 78 99 67
root 92 43 89

cut -d " " -f 1 scores.txt
hacker
root
cut -d " " -f 2 scores.txt
78
92

/challenge/run | cut -d ' ' -f 2 | tr -d '\n'
```
##### sort
The `sort` command helps you organize data. It reads lines from input (or files) and outputs them in sorted order

By default, `sort` orders lines alphabetically. Arguments can change this:
- `-r`: reverse order (Z to A)
- `-n`: numeric sort (for numbers)
- `-u`: unique lines only (remove duplicates)
- `-R`: random order!

```console
sort -r file.txt
```
##### John the Ripper
```console
john ./my-leaked-shadow-file
```
### processes and jobs
ps -ef
ps -aux
ps -jfx

_terminate_ processes:
kill PID
CTRL+C
suspend processes:
CTRL+Z

Resuming Processes(foreground):
команда полностью восстанавливает работу (фоновую или приостановленную)
jobs
fg %n (where `n` is the job number) 
Resuming Processes(background):
переводит в фоновый режим (приостановленную)
bg %n
OR
command & (для не приостановленной)

You can access the exit code of the most recently-terminated command using the special `?` variable (don't forget to prepend it with `$` to read its value!):
echo $?
### users
su user (полный перезаход)
sudo command (единично)
sudo -l (какие привилегии разрешены пользователю)
/etc/passwd (пользователи и данные)
/etc/shadow (пароли пользователей)

ls -la:
тип и права доступа/кол-во ссылок или кол-во подкаталогов для директории/владелец/группа которой принадлежит этот файл/размер/дата и время/название

whoami (кто я)
id (в какой группе я, вторичная группа и тд)

chown - change owner
chgrp - change group
chmod
- `u+s, as above, adds read access to the user's permissions
- `g+wx` adds write and execute access to the group's permissions
- `o-w` _removes_ write access for other users
- `a-rwx` removes all permissions for the user, group, and world
- i=rwx
- -R дать рекурсивно в папке права
### Terminal Multiplexing
##### screen
`screen` is a program that creates virtual terminals inside your terminal. It's somewhat like having multiple browser tabs, but for your command line!
ctrl-D or exit - terminate

`Ctrl-A` is `screen`'s activation key for all of its shortcuts in its default configuration. All `screen` functionality is activated by some command combination starting with `Ctrl-A`.

deteach:
```console
screen
[doing some work...]
[Press Ctrl-A, then d]
[detached from 12345.pts-0.hostname]
```

retach:
```console
screen -ls
There are screens on:
        23847.mysession   (Detached)
        23851.goodwork    (Detached)
        23855.morework    (Detached)
3 Sockets in /run/screen/S-hacker.
```
The identifiers of the sessions are the PID of each respective screen process, a dot, and the name of the screen session. To attach to a specific one, you use its name or its PID by giving it as an argument to `screen -r`.
```console
screen -r goodwork
```

shortcuts for window:
- `Ctrl-A c` - Create a new window
- `Ctrl-A n` - Next window
- `Ctrl-A p` - Previous window
- `Ctrl-A 0` through `Ctrl-A 9` - Jump directly to window 0-9
- `Ctrl-A "` - bring up a selection menu of all of the windows

##### tmux
So to detach from tmux, you press `Ctrl-B` followed by `d`.

```console
tmux
[doing some work...]
[Press Ctrl-B, then d]
[detached (from session 0)] 
```

The commands also differ:
- `tmux ls` - List sessions
- `tmux attach` or `tmux a` - Reattach to session

windows
The key combos are different, but the concept is the same:
- `Ctrl-B c` - Create a new window
- `Ctrl-B n` - Next window
- `Ctrl-B p` - Previous window
- `Ctrl-B 0` through `Ctrl-B 9` - Jump to window 0-9
- `Ctrl-B w` - See a nice window picker

Tmux shows your windows at the bottom in a status bar that looks like:
```
[0] 0:bash* 1:bash
```
### PATH
SET:
```console
PATH=""
ls
bash: ls: No such file or directory
```

where:
which cat
/bin/cat

ADD:
export PATH="/path/ro/dir:$PATH"

### Cимлинк
soft link (Если оригинал удалить, ссылка перестанет работать (станет «битой»)
ln -s /путь/к/оригиналу /путь/к/ссылке

hard link (Это прямой указатель на ту же область данных (inode) на диске, что и сам файл. Для системы жесткая ссылка — это полноценный близнец файла. Если удалить оригинал, данные останутся доступны через жесткую ссылку)
ln /путь/к/оригиналу /путь/к/ссылке
# ***Scriptы***
### variables
**Shell variables** are symbolic names that reference temporary data stored in memory during a shell session or script execution

SYNTAX:
```console
VAR=1337
echo $VAR
#When the shell sees a space, it ends the variable assignment and interprets the next word
VAR="1337 SAUCE"
```

EXPORT: (sh минималистичная реализация командной строки, которая запускается как дочерний процесс вашей основной оболочки)
```console
#By default, variables that you set in a shell session are local to that shell process (другие запускаемые вами команды не унаследуют их)
hacker@dojo:~$ export VAR=1337 (передача в environment variables дочерних процессов)
hacker@dojo:~$ sh
$ echo "VAR is: $VAR"
VAR is: 1337
```
env - печать всех экспортированных переменных

READ:
```
#Here is an example using the `-p` argument, which lets you specify a prompt
read -p "INPUT: " MY_VARIABLE
INPUT: Hello!
#read files/commands
hacker@dojo:~$ echo "test" > some_file
hacker@dojo:~$ read VAR < some_file
hacker@dojo:~$ echo $VAR
test
```

### START

можно написать скрипт и запускать его через нужную нам оболочку:
bash x.sh (This tells bash to read its commands from x.sh)
Но если скрипт исполняем его можно просто запустить без надобности передавать в нужную нам оболочку:
./x.sh (нельзя запускать просто x.sh потому что линукс без указания полного пути ищет builtin команды находящиеся в PATH)

Окей, это всё работает хорошо потому что мы запускаем инструкции из той оболочки из которой нам нужно, а если мы будем совсем в другой оболочке? (кстати, также bash и python не проверяет разрешения файлов) 

когда мы поставим шебанг в начале файла линукс будет рассматривать файл как интерпретируемую программу, а содержимое в остальной части шебанга как путь до интерпретатора. Затем вызывается интерпретатор, передавая ему путь к файлу программы в качестве единственного аргумента
`#!/bin/bash`
`/bin/bash ./script.sh`
или
`#!/usr/bin/python3`
`/usr/bin/python3 ./script.py`

### ARGUMENTS
```console
bash myscript.sh hello world
```
The script can access these arguments using special variables:
- `$1` contains the first argument ("hello")
- `$2` contains the second argument ("world")
- `$3` would contain the third argument (if there had been one)
- and so on

### CONDITIONAL LOGIC
```bash
if [ "$1" == "ping" ]
then
    echo "pong"
fi
```

```bash
if [ "$1" == "hello" ]
then
    echo "Hi there!"
else
    echo "I don't understand"
fi
```

```bash
if [ "$1" == "one" ]
then
    echo "1"
elif [ "$1" == "two" ]
then
    echo "2"
elif [ "$1" == "three" ]
then
    echo "3"
else
    echo "unknown"
fi
```

### WHILE
```bash
while условие; do 
	# команды, которые будут выполняться 
done
```
```bash
while условие
do
	# команды, которые будут выполняться 
done
```

### FOR
```bash
#Выведет числа от 1 до 5 
for i in {1..5} 
do 
	echo "Итерация: $i" 
done 
#Выведет нечетные числа от 1 до 9 (шаг 2)
for i in {1..9..2} 
do 
	echo "Число: $i" 
done
#1, 2, 3
for i in 1 2 3; do echo "Число $i"; done
#счётчик
for ((i=1; i<=5; i++)) 
do 
	echo "Счетчик: $i" 
done
#перебор файлов
for file in *.txt
do
    echo "Обработка файла: $file"
    # mv "$file" "${file%.txt}.bak" (пример переименования)
done
```
### builtins
В операционных системах Linux понятие «builtins» (встроенные команды) относится не к самому ядру Linux, а к **командной оболочке (shell)**, которую вы используете (например, **Bash**, **Zsh** или **Sh**). Эти команды выполняются непосредственно самим командным интерпретатором, а не запускаются как отдельные исполняемые файлы из папок вроде `/bin` или `/usr/bin`.

which echo
echo: shell built-in command

Например:
- `cd` — сменить рабочую директорию.
- `pwd` — вывести текущую рабочую директорию.
- **echo** — Вывести строку текста в терминал.
- **printf** — Форматированный вывод данных (аналог функции в C).
- **export** — Экспортировать переменную в окружение дочерних процессов.
- **unset** — Удалить переменную или функцию.
- **set** — Установить или изменить флаги оболочки и позиционные параметры.
- **umask** — Установить маску создания прав для новых файлов.
- **read** — Прочитать строку со стандартного ввода и записать в переменную.
- **ulimit** — Показать или установить лимиты на системные ресурсы для пользователя.
# Сети
### утилиты
##### ifconfig
Команда ifconfig раньше использовалась для настройки сетевых интерфейсов, однако она устарела. Вместо нее теперь рекомендуется использовать команду ip;
1) Просмотр:
```bash
$ ifconfig
eth0      Link encap:Ethernet  HWaddr 00:1a:2b:3c:4d:5e
          inet addr:192.168.1.100  Bcast:192.168.1.255  Mask:255.255.255.0
          inet6 addr: fe80::21a:2bff:fe3c:4d5e/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:1480304 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1570003 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:2207584244 (2.2 GB)  TX bytes:2037489282 (2.0 GB)
```
eth0: Это имя интерфейса (может быть другим, например, wlan0 для беспроводных соединений).

inet addr:192.168.1.100: IP-адрес интерфейса.

Mask:255.255.255.0: Маска подсети.

RX packets: Полученные пакеты.

TX packets: Отправленные пакеты.

2) Настройка IP-адреса вручную:
```bash
ifconfig eth0 192.168.1.101 netmask 255.255.255.0 up
```
Эта команда назначает IP-адрес 192.168.1.101 на интерфейс eth0 с маской подсети 255.255.255.0. Ключ up активирует интерфейс.

3) Отключение сетевого интерфейса
```bash
ifconfig eth0 down
```
Команда отключает интерфейс eth0
##### ip
1) ip addr show - Отображение информации о сетевых интерфейсах

```bash
$ ip addr show

3: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 00:1a:2b:3c:4d:5e brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.100/24 brd 192.168.1.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::21a:2bff:fe3c:4d5e/64 scope link
       valid_lft forever preferred_lft forever
```

inet 192.168.1.100/24: IP-адрес и маска подсети.

inet6 fe80::21a:2bff:fe3c:4d5e/64: IPv6-адрес.

2) Настройка IP-адреса вручную
ip addr add 192.168.1.101/24 dev eth0
Эта команда назначает IP-адрес 192.168.1.101 с маской подсети /24 на интерфейс eth0.

3) Удаление IP-адреса с интерфейса
ip addr del 192.168.1.101/24 dev eth0

4) Включение сетевого интерфейса
ip link set eth0 up

5) Отключение сетевого интерфейса
ip link set eth0 down

6) Проверка маршрутов
```bash
$ ip route show

default via 192.168.1.1 dev eth0
192.168.1.0/24 dev eth0 scope link
```
default via 192.168.1.1 dev eth0: Этот маршрут указывает, что все пакеты, не имеющие специфического маршрута, будут отправляться через шлюз 192.168.1.1 по интерфейсу eth0.

192.168.1.0/24 dev eth0 scope link: Локальная сеть 192.168.1.0/24 доступна через интерфейс eth0.

##### nmcli
nmcli - это инструмент для управления сетевыми соединениями с использованием NetworkManager. Он позволяет настраивать сети, подключаться к Wi-Fi и управлять всеми типами сетевых соединений.

1) Проверка состояния сетевых соединений
```bash
$ nmcli device status

DEVICE  TYPE      STATE        CONNECTION
eth0    ethernet  connected    Wired connection 1
wlan0   wifi     disconnected  --
```
Показывает текущее состояние всех сетевых устройств. В примере eth0 подключен через проводное соединение, а wlan0 не подключен.

2) Список доступных Wi-Fi сетей
$nmcli device wifi list
Список доступных Wi-Fi сетей с показателями уровня сигнала, скорости и типа безопасности.

3) Подключение к Wi-Fi сети
```bash
nmcli device wifi connect MyWiFiNetwork password mypassword
```

MyWiFiNetwork с паролем mypassword. Если все прошло успешно, nmcli выведет сообщение о подключении.

4) Проверка активных соединений
```bash
$ nmcli connection show

NAME                UUID                                  TYPE            DEVICE
Wired connection 1  12345678-abcd-1234-5678-abcd12345678  ethernet        eth0
MyWiFiNetwork       87654321-dcba-4321-8765-dcba87654321  wifi            wlan0
```

5) Создание нового Wi-Fi соединения и подключение (то же самое что и в 3, но теперь вручную, а не автоматически)
```zsh
nmcli connection add type wifi con-name MyNewWiFi ifname wlan0 ssid MyWiFiNetwork

nmcli connection modify MyNewWiFi wifi-sec.key-mgmt wpa-psk

nmcli connection modify MyNewWiFi wifi-sec.psk "mypassword"

nmcli connection up MyNewWiFi

```
Создает новое подключение для Wi-Fi сети с SSID MyWiFiNetwork и паролем mypassword.

##### traceroute
traceroute - отображение пути до удаленного хоста (не всегда правдиво тк один из узлов может поменять ttl пакета и отправить его дальше). \* - пакет не дошёл до нас
```bash
$ traceroute example.com

traceroute to example.com (93.184.216.34), 30 hops max, 60 byte packets
 1  192.168.1.1  1.120 ms  1.104 ms  1.085 ms
 2  10.10.10.1  5.350 ms  5.343 ms  5.318 ms
 3  172.16.1.1  10.560 ms  10.540 ms  10.515 ms
 4  93.184.216.34  20.645 ms  20.622 ms  20.598 ms
```
Показывает путь, который проходят пакеты от вашего компьютера до удалённого хоста example.com, включая промежуточные маршрутизаторы.

##### netstat/ss
netstat/ss - просмотр активных соединений и портов

Использование:
netstat/ss -tuln (для нормисного вывода)
netstat/ss (для нормального вывода)

##### tcpdump
**tcpdump** — это консольная утилита для перехвата и анализа сетевых пакетов в реальном времени
sudo tcpdump -i <интерфейс> \[опции\] \[фильтр\]

```
-i <iface> — слушать конкретный интерфейс (например, `eth0` или `any` для всех).

-n / -nn — не преобразовывать IP-адреса в имена хостов (`-n`) и номера портов в названия служб (`-nn`).

-c <N> — остановить захват после получения `N` пакетов.

-tttt — выводить полную дату и время в читаемом виде.

-w <file.pcap> — сохранить трафик в файл для последующего разбора (например, в Wireshark).

-r <file.pcap> — прочитать пакеты из сохранённого файла.

port <N> - только входящий и исходящий трафик по порту N

-G <N> - интервал ротации в секундах. Утилита закрывает текущий дамп и открывает новый файл каждые N секунд
```
tcpdump -i eth0 -G 180 -w "traffic_%H:%M:%S.pcap" port 8080
# ***СИС АДМ***
#### ЧЗХ
Хорошая автоматизация должна быть:
- **повторяемой** — одинаковый запуск даёт предсказуемый результат;
- **наблюдаемой** — можно понять, что произошло;
- **безопасной при ошибках** — сбой одной операции не должен приводить к повреждению системы.
Основные задачи администратора:
- резервное копирование;
- мониторинг;
- управление пакетами и обновлениями;
- настройка служб;
- оптимизация ресурсов;
- автоматизация;
- удалённое администрирование.
#### Резервное копирование
`rsync` позволяет синхронизировать каталоги:
```bash
rsync -av --delete /home/username/ /backup/username/
```
- `-a` — архивный режим;
- `-v` — подробный вывод;
- `--delete` — удалить из бэкапа файлы, которых больше нет в источнике.
можно делать бекапы с помощью cron
#### Мониторинг системы
1) htop
2) journalctl -u \<service\> (or journalctl -xe)
3) systemctl status \<service\>
4) df
#### Управление пакетами и обновления

Для Debian/Ubuntu используется `apt`:
```
sudo apt update && sudo apt upgrade -y
```
Очистка кэша (установочные файлы):
```
sudo apt clean
sudo apt autoclean
```
Удаление ненужных зависимостей (осиротевшие библиотеки):
```
sudo apt autoremove
```
Автоматические обновления безопасности можно настроить через:
```
sudo apt install unattended-upgrades (запускает автоматическую фоновую загрузку и установку важных обновлений безопасности без участия пользователя)

sudo dpkg-reconfigure --priority=low unattended-upgrades (Флаг `--priority=low` принудительно открывает текстовое меню в терминале, где пользователю задается вопрос: «Хотите ли вы автоматически скачивать и устанавливать обновления безопасности?»)
```
#### Cron
cron запускает команды и скрипты по расписанию.
Редактирование заданий:
crontab -e

Формат:
минута час день_месяца месяц день_недели команда

Примеры:
- 0 2 * * * /path/to/script.sh
Каждый день в 02:00.

- \*/5 * * * * /path/to/script.sh
Каждые 5 минут.
#### Systemd
`systemd` управляет службами Linux.
Основные команды:
```
sudo systemctl start service
sudo systemctl stop service
sudo systemctl restart service
sudo systemctl status service
sudo systemctl enable service
```
После изменения unit-файлов:
```
sudo systemctl daemon-reload
```
unit-файлы — это текстовые файлы настроек, которые объясняют системе инициализации (в большинстве современных дистрибутивов Linux это **`systemd`**) как именно нужно управлять конкретной программой, скриптом или процессом.
