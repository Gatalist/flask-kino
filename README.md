### Run locally:
Run in terminal:
`docker compose -f docker-compose.yml up --build`  

### migrations:
Run in terminal:
`docker exec -it flask_app /bin/bash`
`flask db init`
`flask db migrate`
`flask db upgrade`

### iptables for wireguard:
Run in terminal:
`sudo dnf install iptables iptables-legacy`
`sudo modprobe ip_tables`

### permission for folder on use in docker:
Run in terminal (for folder accesses):
`sudo chcon -Rt svirt_sandbox_file_t ./wireguard/config/us/`

### install in server 
`sudo dnf install iptables-legacy`
`sudo alternatives --set iptables /usr/sbin/iptables-legacy`
`sudo alternatives --set ip6tables /usr/sbin/ip6tables-legacy`
`sudo systemctl restart docker`