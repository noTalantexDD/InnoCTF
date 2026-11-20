# InnoCTF
InnoCTF Junior заключительный этап

# Начало на ноутбуках
1. Поменять пароли на kali
2. Удалить лишние ssh ключи
   Убрать подключение по паролю
systemctl is-active ssh      # должно быть inactive
ss -tlnp | grep :22          # пусто
sudo systemctl disable --now ssh ssh.socket 2>/dev/null
4. Добавить свои ключи
