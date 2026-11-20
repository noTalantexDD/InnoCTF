# тшка 
1) Сообщение зашифровано аффинным шифром над английским алфавитом a=0…z=25 по формуле C=(9·P+14) mod 26. Расшифруйте `obueyl hkl gitzyl iu uygmlidw` и укажите только последнее слово.

находим решение уравнения: (C+26k - 14)/9 = P, где 0<=P<26, k-параметр модуля
```c++
#include <iostream>
using namespace std;
int main() {
    string t = "obueylhklgitzyliuuygmlidw";
    int P = -1;
    int k = 0;

    for (int i = 0; i < t.size(); i++){
        while(!(P < 26 && P >= 0)){
            if((int(t[i]) - 97 + 26*k - 14) % 9 == 0){
                P = (26*k + t[i] - 97 - 14)/9;
                if(P < 26 && P >= 0){
                    cout << char(P+97);
                }
                else{
                    k++;
                }
            }else{
                k++;
            }
        }
        P = -1;
        k = 0;
    }
    return 0;
}
```
answer for cipher security

2) Используйте шифр Атбаш для английского алфавита a–z: a↔z, b↔y, …, пробелы сохраняются, ответ — строчными буквами. Зашифруйте: `cybersecurity is a popular science`
строчные латинские символы в ASCII начинаются с 97, в латинском алфавите 26 букв
```c++
#include <iostream>

using namespace std;

int main() {
    string t = "cybersecurityisapopularscience";

    for (int i = 0; i < t.size(); i++){
        cout << char(26 - (int(t[i]) - 97) + 96);
    }
    
    return 0;
}
```

3) Текст зашифрован учебной реализацией шифра Гронсфельда над английским алфавитом a–z. Цифры ключа 2025 циклически задают сдвиг букв вперёд; позиция ключа увеличивается на каждом символе, включая пробел, хотя сам пробел не изменяется. Расшифруйте deuy cnfuskh ctdrtq gvgw и укажите всю фразу строчными буквами.
```c++
int main(){
    string t = "deuy cnfuskh ctdrtq gvgw";
    string key = "2025";

    for (int i = 0; i < t.size(); i++){
        if(t[i] != ' '){
            if(int(t[i]) - (int(key[i%key.size()]) - 48)< 97){
                t[i] = char(int(t[i]) - (int(key[i%key.size()]) - 48) + 26);
            }else{
                t[i] = char(int(t[i]) - (int(key[i%key.size()]) - 48));
            }
        }
    }
    
    cout << t;
    return 0;
}
```