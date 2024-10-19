
"""
Create users in Authentik from a given list as CSV file.

Requirements:
 - requests

Sources:
 - https://docs.goauthentik.io/docs/developer-docs/api/reference/core-users-create
 - https://docs.goauthentik.io/docs/developer-docs/api/reference/core-users-set-password-create
"""

import json

import yaml
import requests


BASE_URL = 'https://auth.brinkstrasse.schule'


def import_user_list():
    import csv
    with open('user_list.csv', newline='') as f:
        reader = csv.reader(f)
        result = [list((e.strip() for e in row)) for row in reader]
    return result


def load_API_token():
    with open('../group_vars/all.yml', 'r') as file:
        ansible_group_vars = yaml.safe_load(file)
        TOKEN = ansible_group_vars['services']['authentik']['token']
        print(f'Loaded token from Ansible group variables: {TOKEN}')
    return TOKEN

TOKEN = load_API_token()

def create_user(name, username, email, groups=()):
    print(f'Creating user {username}...')
    url = f'{BASE_URL}/api/v3/core/users/'
    payload = json.dumps({
        'username': username,
        'name': name,
        'is_active': True,
        'email': email,
        'type': 'internal'
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }
    response = requests.request('POST', url, headers=headers, data=payload)
    #print(response.text)
    print(f'Created user {username} with email {email} and assigned user id {response.json()["pk"]}')
    return response.json()["pk"]


def set_user_password(userid, password):
    print(f'Setting password for user no. {userid}...')
    url = f'{BASE_URL}/api/v3/core/users/{userid}/set_password/'
    payload = json.dumps({
        'password': password
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }
    response = requests.request('POST', url, headers=headers, data=payload)
    print(response.text)


def create_group(name):
    print(f'Creating group {name}...')
    url = f'{BASE_URL}/api/v3/core/groups/'
    payload = json.dumps({
        'name': name,
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }
    response = requests.request('POST', url, headers=headers, data=payload)
    print(response.text)


def list_users():
    print('Listing users...')
    url = f'{BASE_URL}/api/v3/core/users/'
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }
    response = requests.request('GET', url, headers=headers, data=payload)
    print(json.dumps(response.json(), indent=4))


def list_groups():
    print('Listing groups...')
    url = f'{BASE_URL}/api/v3/core/groups/'
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }
    response = requests.request('GET', url, headers=headers, data=payload)
    print(json.dumps(response.json(), indent=4))


#list_users()
#list_groups()
for firstname, surname, email, username, password, group in import_user_list():
    userid = create_user(f'{firstname} {surname}', username, email)
    set_user_password(userid, password)
