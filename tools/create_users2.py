
"""
Create users in Authentik from a given list as CSV file.

Requirements:
 - authentik_client

Source:
 - https://pypi.org/project/authentik-client/
"""


import csv
import yaml

import authentik_client
from authentik_client.rest import ApiException


def import_user_list_csv():
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


configuration = authentik_client.Configuration(
    host='https://auth.brinkstrasse.schule/api/v3',
    access_token=load_API_token()
)


def list_users(core_api):
    api_response = core_api.core_users_list()
    print('The response of core_users_list:')
    for u in api_response.results:
        print(u.username, u.name, u.email)


def create_user(core_api, name, username, email):
    print(f'Creating user {username}...')
    api_response = core_api.core_users_create(
        user_request={'name': name, 'username': username, 'email': email}
    )
    #print(api_response)
    print(f'Created user {api_response.username} with email {api_response.email} and assigned user id {api_response.pk}')
    return api_response.pk


def set_user_password(core_api, userid, password):
    print(f'Setting password for user no. {userid}...')
    api_response = core_api.core_users_set_password_create(
        id=userid, user_password_set_request={'password': password}
    )
    #print(api_response)


def main():
    with authentik_client.ApiClient(configuration) as api_client:
        core_api = authentik_client.CoreApi(api_client)
        try:
            # list_users(core_api)
            for firstname, surname, email, username, password, group in import_user_list_csv():
                userid = create_user(core_api, f'{firstname} {surname}', username, email)
                set_user_password(core_api, userid, password)
        except ApiException as e:
            print('Exception when calling AdminApi->admin_apps_list: %s\n' % e)


main()
