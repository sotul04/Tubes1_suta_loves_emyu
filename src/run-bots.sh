#!/bin/bash

python3 main.py --logic Machine --email=main@email.com --name=main --password=123456 --team etimo &
python3 main.py --logic Machine --email=bot1@email.com --name=bot1 --password=123456 --team etimo &
python3 main.py --logic Machine --email=bot2@email.com --name=bot2 --password=123456 --team etimo &
python3 main.py --logic Machine --email=bot3@email.com --name=bot3 --password=123456 --team etimo &