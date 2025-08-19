
"""
List and create mail accounts on a Stalwart mail server.

Sources:
 - https://stalw.art/docs/api/management/endpoints
"""

import argparse
from logging import DEBUG

import httpx
from rich.console import Console
from rich.table import Table


DEBUG = False
mail_server = ''
api_user = ''
api_password = ''


headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}


def list_mail_accounts():
  console = Console()
  table = Table(show_header=True, header_style="bold")
  table.add_column('Id')
  table.add_column('Type')
  table.add_column('Name')
  with httpx.Client(auth=(api_user, api_password)) as client:
    r = client.get(f'https://{mail_server}/api/principal', headers=headers)
  for u in r.json()['data']['items']:
     table.add_row(str(u['id']), u['type'], u['name'])
  console.print(table)


def create_mail_account(name, email, password):
  body = {
    'type': 'individual',
    'quota': 1024 ** 3,
    'name': email,
    'description': name,
    'secrets': [password,],
    'emails': [email,],
    'urls': [],
    'memberOf': [],
    'roles': ['user'],
    'lists': [],
    'members': [],
    'enabledPermissions': [],
    'disabledPermissions': [],
    'externalMembers': []
  }
  with httpx.Client(auth=(api_user, api_password)) as client:
      r = client.post(f'https://{mail_server}/api/principal', headers=headers, json=body)
  if DEBUG:
    print(r.json())


def main():
  parser = argparse.ArgumentParser(description='Account management for Stalwart mail server')
  parser.add_argument('name', type=str, help='Name for new user')
  parser.add_argument('email', type=str, help='Email for new user')
  parser.add_argument('password', type=str, help='Password for new user')
  parser.add_argument('-l', '--list', action='store_true', help='Output list of all users')
  args = parser.parse_args()
  create_mail_account(args.name, args.email, args.password)
  if args.list:
    list_mail_accounts()


if __name__ == '__main__':
  main()
