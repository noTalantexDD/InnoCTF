# first settings
Before starting the stack, edit `services/api/configurations.py`:

```python
vm_ip = "10.60.4.1"
services = [{"ip": vm_ip, "port": 18080, "name": "BIOMarkt"},
            {"ip": vm_ip, "port": 5555, "name": "SaaS"},
]
```

You can also edit this during the CTF, just rebuild the `api` service:

```bash
docker compose up --build -d api
```


# Usage
The stack can be started with docker-compose, after creating an `.env` file. See `.env.example` as an example of how to configure your environment.

```bash
cp .env.example .env
# < Edit the .env file with your favourite text editor >
docker compose up -d --build
```

To ingest traffic, it is recommended to create a shared bind mount with the docker-compose. One convenient way to set this up is as follows:

1. On the vulnbox, start a rotating packet sniffer (e.g. tcpdump, suricata, ...)

```shell
sudo tcpdump -i eth0 -G 180 -Z root -w /path/to/file/traffic_%H:%M:%S.pcap port 8080
```

2. Using rsync, copy complete captures to the machine running tulip (e.g. to /traffic)

```shell
rsync -avz -e ssh --progress root@10.0.0.0:/pcaps ./pcaps
```

3. Add a bind to the assembler service so it can read /traffic
    
    > (Just change `TRAFFIC_DIR_HOST` in `.env`)
    

The ingestor will use inotify to watch for new pcap's and suricata logs. No need to set a chron job.

