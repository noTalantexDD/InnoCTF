# Настройка подключения по ssh
1. ssh-keygen -t ed25519 -C "menadBANDIT@innopolis.com"
2. ssh-copy-id -i .../ваш_ключ.pub username@server_ip
3. chmod 700 на приватный ключ (на публичный, если автоматически не применилось)

P.S.
2. Если вдруг не сработал ssh-copy-id, то делаем вручную
 - mkdir -p ~/.ssh && chmod 700 ~/.ssh
 - echo "ваш_публичный_ключ_целиком" >> ~/.ssh/authorized_keys
 - chmod 600 ~/.ssh/authorized_keys


# Отключение пароля от root на сервере
1. sudo nano /etc/ssh/sshd_config
2. 'PermitRootLogin prohibit-password'
3. Вот это 
```sudo tee /etc/ssh/sshd_config.d/99-disable-root-password.conf > /dev/null << 'EOF'
PermitRootLogin prohibit-password
PasswordAuthentication no
EOF```
4. Перезапуск ssh
```sudo systemctl restart ssh```

