#!/usr/bin/env python3

import sys

try:
    import dotenv
except:
    print(f"Please run `{sys.executable} pip install -r requirements.txt` to install requirements.", file=sys.stderr)
    sys.exit(1)

token = input("Enter your bot token (leave blank to keep it unchanged): ").strip()
prefix = input("Enter the command prefix (leave blank to use default `lru!`): ").strip()

if prefix == '':
    prefix = 'lru!'

if token != '':
    dotenv.set_key('.env', 'token', token)

dotenv.set_key('.env', 'prefix', prefix)
