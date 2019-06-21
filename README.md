Service for relaying [WOL](https://en.wikipedia.org/wiki/Wake-on-LAN) signals outside docker container without enabling net host flag.

## Instalation
```
sudo cp systemd/mqtt2wol.service /lib/systemd/system/
sudo systemctl enable mqtt2wol.service
```
