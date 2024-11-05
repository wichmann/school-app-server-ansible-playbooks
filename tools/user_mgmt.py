
"""
Manage users in Authentik by command line.

Requirements:
 - authentik_client

Source:
 - https://pypi.org/project/authentik-client/
"""


import sys
import csv
import yaml
import random
import logging
import logging.handlers

import fire
import authentik_client
from authentik_client.rest import ApiException


PASSWORD_LENGTH = 12
LOG_FILENAME = 'user_mgmt.log'

# create logger for this application
logger = logging.getLogger('user_mgmt')
logger.setLevel(logging.DEBUG)
log_to_file = logging.handlers.RotatingFileHandler(
    LOG_FILENAME, maxBytes=262144, backupCount=5, encoding='utf-8')
log_to_file.setLevel(logging.DEBUG)
logger.addHandler(log_to_file)
log_to_screen = logging.StreamHandler(sys.stdout)
log_to_screen.setLevel(logging.INFO)
logger.addHandler(log_to_screen)


def import_user_list_csv():
    with open('user_list.csv', newline='') as f:
        reader = csv.reader(f)
        result = [list((e.strip() for e in row)) for row in reader]
    return result


def generate_good_readable_password():
    """
    Generate a random password for a given length including all letters and
    digits. This password contains at least one lower case letter, one upper
    case letter and one digit. To generate unpredictable passwords, the
    SystemRandom class from the random module is used! All ambiguous characters
    are exempt from passwords.

    Source: https://stackoverflow.com/questions/55556/characters-to-avoid-in-automatically-generated-passwords

    :return: string containing random password of good quality
    """
    password = []
    # define possible characters for use in passwords (source: https://www.grc.com/ppp.htm)
    uppercase = 'ABCDEFGHJKLMNPRSTUVWXYZ'
    lowercase = 'abcdefghijkmnopqrstuvwxyz'
    digits = '23456789'
    chars = uppercase + lowercase + digits
    # fill up with at least one uppercase, one lowercase and one digit
    password += random.SystemRandom().choice(uppercase)
    password += random.SystemRandom().choice(lowercase)
    password += random.SystemRandom().choice(digits)
    # fill password up with more characters
    password += [random.SystemRandom().choice(chars)
                 for _ in range(PASSWORD_LENGTH-3)]
    # shuffle characters of password string
    random.shuffle(password)
    logger.debug('New password generated: ' + ''.join(password))
    return ''.join(password)


class UserManagement:
    def __init__(self):
        self._load_configuration()
        configuration = authentik_client.Configuration(
            host=self._host,
            access_token=self._token
        )
        self._api_client = authentik_client.ApiClient(configuration)
        self._core_api = authentik_client.CoreApi(self._api_client)

    def _load_configuration(self):
        with open('../host_vars/server-it-01.yml', 'r') as file:
            ansible_host_vars = yaml.safe_load(file)
            token = ansible_host_vars['services']['authentik']['token']
            base_domain = ansible_host_vars['basedomain']
            logger.debug(f'Loaded token from Ansible group variables: {token}')
        with open('../group_vars/all.yml', 'r') as file:
            ansible_group_vars = yaml.safe_load(file)
            authentik_domain = ansible_group_vars['subdomains']['authentik']
        self._token = token
        self._host = f'https://{authentik_domain}.{base_domain}/api/v3'

    def _list_users(self):
        api_response = self._core_api.core_users_list()
        result = []
        for u in api_response.results:
            result.append((u.username, u.name, u.email))
        return result

    def _list_groups(self):
        api_response = self._core_api.core_groups_list()
        #print('The response of core_groups_list: ', api_response)
        return api_response.results

    def _create_user(self, name, username, email):
        print(f'Creating user {username}...')
        api_response = self._core_api.core_users_create(
            user_request={'name': name, 'username': username, 'email': email}
        )
        # print(api_response)
        print(f'Created user {api_response.username} with email {api_response.email} and assigned user id {api_response.pk}')
        return api_response.pk

    def _find_group_id(self, group_name: str):
        return [g for g in self._list_groups() if g.name == group_name][0].pk

    def _create_group_for_class(self, group_name):
        logger.debug(f'Creating group {group_name}...')
        parent_group = self._find_group_id('Schülerinnen und Schüler')
        api_response = self._core_api.core_groups_create(
            user_request={'name': name, "is_superuser": False, 'parent': parent_group}
            # "users": [ 0 ],
        )
        # print(api_response)
        print(f'Created group {api_response.name} with id {api_response.pk}')
        return api_response.pk

    def _set_user_password(self, userid, password):
        print(f'Setting password for user no. {userid}...')
        api_response = self._core_api.core_users_set_password_create(
            id=userid, user_password_set_request={'password': password}
        )
        # print(api_response)

    def _add_user_to_group(self, userid, group_name):
        print(f'Adding user no. {userid} to group "{group_name}"...')
        try:
            group_id = self._find_group_id(group_name)
            api_response = self._core_api.core_groups_add_user_create(
                group_uuid=group_id, user_account_request={'pk': userid}
            )
        except ApiException as e:
            print('Exception while adding user to group: %s\n' % e)

    def import_user(self, filename: str):
        """
        Import a list of users from a CSV file. The file must have the following
        columns: 'firstname', 'surname', 'email', 'username', 'password', 'group'.
        """
        try:
            for firstname, surname, email, username, password, group in import_user_list_csv():
                userid = self._create_user(f'{firstname} {surname}', username, email)
                self._set_user_password(userid, password)
                # TODO: Add user to group
        except ApiException as e:
            print('Exception while importing users: %s\n' % e)

    def add_teacher(self, surname: str, firstname: str, email: str, username: str):
        """
        Add a single user to Authentik and assign to group of teachers.
        """
        try:
            password = generate_good_readable_password()
            userid = self._create_user(f'{firstname} {surname}', username, email)
            print(f'Password for new user {username} is "{password}"!')
            self._set_user_password(userid, password)
            self._add_user_to_group(userid, 'Lehrerinnen und Lehrer')
        except ApiException as e:
            print('Exception when calling AdminApi->admin_apps_list: %s\n' % e)


if __name__ == '__main__':
    logger.debug('Starting user_mgmt...')
    fire.Fire(UserManagement)
