это технология контейнеризации
сервисы находятся в docker-контейнерах (специальной среде исполнения, которая изолирует сервисы друг от друга) 
docker image - как контейнер создать и расплодить. Образ по которому контейнер был создан
# установка
```bash
sudo apt update  
sudo apt install ca-certificates curl  
sudo install -m 0755 -d /etc/apt/keyrings  
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc  
sudo chmod a+r /etc/apt/keyrings/docker.asc  
  
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF  
Types: deb  
URIs: https://download.docker.com/linux/debian  
Suites: $(. /etc/os-release && echo "trixie")  
Components: stable  
Architectures: $(dpkg --print-architecture)  
Signed-By: /etc/apt/keyrings/docker.asc  
EOF  
  
sudo apt update

sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

# запуск
docker compose up -d --build (в папке где находится управляющий .yml/.yaml файл)
не забыть дать права папке где контейнер находится:
chmod -R a+rX ~/docker/...

запуск по другому:
	docker build /path/to/image -t <name\>
	docker run <name\> 
Рестарт:
	docker restart <name\>
# взаимодействие с контейнерами
Логи контейнера:
docker compose logs -f <имя сервиса>/docker logs

Информация о контейнерах:
docker ps
	Важное:
	• CONTAINER ID. Короткий уникальный идентификатор контейнера.
    • IMAGE. Название и тег образа, из которого был создан контейнер.
    • COMMAND. Команда, запущенная внутри контейнера при его старте.

запустить исполняемый файл внутри контейнера:
	docker exec -it <имя сервиса> <команда>

посмотреть инфу про образы(dockerfile):
	docker images
		Важное:
		REPOSITORY - название образа
		TAG - версия образа
# остановка
остановка всех контейнеров
docker compose down

docker stop \<id>

# dockerfile
что нужно сделать чтобы этот контейнер(или приложение внутри контейнера) запустить
на dockerhub можно использовать шаблоны образов

docker run kitematic/minecraft

потом будет как их создавать мб. Самая важная часть так то