# BASE
**data type**
```c
int
float
double
char
bool
long long
```
**input/output**
```c
puts(""); //вывести в stdout, уязвимо
gets(buf) //записать в buf stdin c \n 

//Formatted
printf() //выводит данные на экран (в поток `stdout`).
scanf() //считывает данные с клавиатуры (из потока `stdin`). При чтении переменных обязательно передается их адрес в памяти с помощью оператора &
	//example:
	int age; printf("Введите ваш возраст: "); 
	scanf("%d", &age); // Чтение числа и запись по адресу переменной &age 
	printf("Ваш возраст: %d\n", age); // Форматированный вывод return 0;

//Unformatted
char ch; 
ch = getchar(); // Считывает символ, например 'A'
putchar(ch); // Выводит 'A' на экран

//Функция `scanf("%s", ...)` считывает текст только до первого пробела. Чтобы безопасно считывать и выводить полноценные строки с пробелами, используют:
fgets(buffer, size, stdin) //считывает строку целиком (включая пробелы), предотвращая переполнение буфера.
//example
	char name[50]
	fgets(name, sizeof(name), stdin);
```
- `%d` — целые числа со знаком (`int`)
- `%f` — числа с плавающей точкой (`float`)
- `%c` — один символ (`char`)
- `%s` — строка символов (слово)
# Library
```c
1) #include <stdlib.h>
Standard Library(управление памятью, генерация случайных чисел, контроль выполнения программы и system!!!)

2) #include <sys/types.h>
- pid_t — тип данных для идентификаторов процессов (PID)
- size_t — тип для размеров объектов в памяти
- mode_t — тип для задания прав доступа к файлам
- time_t — тип для работы со временем

3) #include <unistd.h> 
(POSIX OS API)
- Функции для создания процессов: fork()
- Замена текущего процесса другим: функции семейства exec (например, execl(), execvp())
- Получение ID текущего процесса: getpid()
- Низкоуровневая работа с файлами: read(), write(), close()
- Пауза в выполнении программы: sleep()
  
4) #include <stdio.h>
-работа с вводом и выводом

5) #include <string.h>
```

# Linux/CS:
```c
1) setreuid(geteuid(), geteuid()); //(выполняется исключительно в пределах текущего процесса)

//Этот трюк часто применяется в SUID-программах (программах, которые принадлежат root, но запускаются обычными пользователями)

- geteuid() — возвращает эффективный UID (Effective User ID) текущего процесса. Именно этот ID определяет, к каким файлам и системным ресурсам у процесса есть доступ прямо сейчас.
- setreuid(ruid, euid) — устанавливает реальный UID (Real UID — кто запустил программу) и эффективный UID (Effective UID) процесса.
  
2) system(); - bin/sh -c
3) read(fd, buf, 32); //read(file descriptor, where do we write, max number of bytes that can be read) //return >0 -> number of bytes actually read //return 0 -> channel is closed/EOF //return -1 error occurred
```
# Struct
```c
//В Си `struct` — это составной тип данных, который объединяет несколько переменных (полей) разных типов в один непрерывный блок памяти. Крч, это класс без методов(а в с++ это реально класс, но только всегда public)

struct Point {
    int x;
    int y;
};
struct Point p1;
//обращение к полям
p1.x = 1;
p1.y = 2;
//или
struct Point = {.x = 1, .y = 2};
```

# strings
```c
//строки задаются как массивы
char s[]="Hello"; //C-строка массив + "\0" (терминирующий ноль)
std::string s = "Hello"; //std-строка
s+="asd";
s[0] = "a";

strlen("asd"); //string length, return 3
strcmp("LETMEWIN\n", buf); //return 0 if strings are equals
atoi("123"); //ascii to int, return int(123)
```
# array
```c
char buf[32] = {0}; //(заполнить массив чаров нулями)

//static arr
int a[5] = {1, 2, 3, 4, 5};

//vector
#include <vector> 
std::vector<int> vec = {1, 2, 3}; 
vec.push_back(4);

//dynamic arr
//size - const
int* dynArr = new int[size];
delete[] dynArr;
```

# pointers
```c
int x = 10; 
int *p = &x; // указатель p хранит адрес переменной x
*p = 20; // изменяет значение x на 20
```
**Изменение аргументов в функции.** В Си аргументы передаются по значению (функция работает с копией). Чтобы изменить саму переменную, в функцию передают её адрес:
```c
void add_one(int *n) {
    (*n)++;
}
```
**Имя массива в Си неявно преобразуется в указатель на его первый элемент (`&arr[0]`).**
```c
int* ip = (int*)p; //если p это имя массива например char, то ip это указатель на тот же массив, только элементы будут читаться из массива как int значения (при этом память "склеится", 4 элемента char станут 1 элементом int. см в pwn)
```
# args
```c
#include <stdio.h> 
int main(int argc, char *argv[]){ 
	//xnjnj
	return 0; 
}
argc - argument count
//имя самой запущенной программы считается первым аргументом, поэтому значение argc всегда как минимум равно 1

argv (Argument Vector): Массив указателей на строки (массив строк), содержащий сами аргументы.
    - argv[0] — имя исполняемого файла программы
    - argv[1] — первый пользовательский аргумент.
    - argv[2] — второй пользовательский аргумент и так далее.
    - argv[argc] — всегда равен `NULL` (маркер конца массива)
      
gcc app.c -o app 
./app hello world 123
```

# malloc/free/calloc/realloc
• malloc(size_t size) — выделяет блок размером size байт без очистки содержимого (в байтах остаётся «мусор»). Возвращает 
void * или NULL при ошибке.

• calloc(size_t nmemb, size_t size) — выделяет память под nmemb элементов по size байт каждый и заполняет все байты нулями (0). Возвращает void * или NULL.

• realloc(void *ptr, size_t size) — меняет размер ранее выделенного блока ptr до size байт. При расширении может переместить блок в другое место и скопировать старые данные. Если ptr == NULL, работает как malloc(size). При ошибке возвращает NULL, а исходный блок ptr остаётся нетронутым.

• free(void *ptr) — освобождает память, выделенную malloc, calloc или realloc. Если передать NULL, ничего не делает.




