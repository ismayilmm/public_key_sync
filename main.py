import os
import pysftp
import shutil
import logging

hosts = []
current_dir = '/home/mmd/PycharmProjects/public_key_sync'
log_file = open('ssh_sync_log', 'a')


def open_main_file(file='main_file_for_keys'):
    with open(file) as main_file:
        main_file_lines = main_file.readlines()
    return main_file_lines


def read_host_file(file='hosts'):
    return store_host_names(open_file())


def open_file(file='hosts'):
    hosts_file = open(file, 'r')
    hosts_credentials = hosts_file.readlines()
    return hosts_credentials


def store_host_names(host_file):
    for i, line in enumerate(host_file):
        split_by_space = line.split(' ')
        hostname = split_by_space[0]
        username = split_by_space[1]
        password = format_the_string(split_by_space[2])
        hosts.append((hostname, username, password))
        log_file.write("Successful read of keys for the host: " + split_by_space[1] + "@" + split_by_space[0] + "\n")
    return hosts


def format_the_string(string):
    size = len(string)
    mod_string = string[:size - 1]
    return mod_string


def get_authorized_keys(hostname, username, password):
    path_to_file = '/home/' + username + '/.ssh'
    with pysftp.Connection(hostname, username=username, password=password) as sftp:
        with sftp.cd(path_to_file):
            sftp.get('authorized_keys')
    sftp.close()


def sync_auth_keys_with_main_file(main_file_lines, file_name='authorized_keys', main_file='main_file_for_keys'):
    with open(file_name) as file:
        auth_file = file.readlines()
        for line in auth_file:
            if compare_line_to_file(line, main_file_lines) is False:
                write_to_file(line, main_file)
    os.remove(file_name)


def compare_line_to_file(check_line, main_file_lines):
    check = False
    for line in main_file_lines:
        if line == check_line:
            check = True
    return check


def write_to_file(authorized_keys, file='main_file_for_keys'):
    file = open(file, 'a')
    file.write(authorized_keys)
    file.close()


def create_updated_file(old_name='main_file_for_keys', new_name='authorized_keys'):
    shutil.copy(old_name, current_dir + "/" + new_name)


def update_hosts(hostname, username, password):
    path_to_file = '/home/' + username + '/.ssh'
    with pysftp.Connection(hostname, username=username, password=password) as sftp:
        with sftp.cd(path_to_file):
            sftp.put('authorized_keys')
    sftp.close()


def main():
    hosts = read_host_file()
    for host in hosts:
        get_authorized_keys(hostname=host[0], username=host[1], password=host[2])
        sync_auth_keys_with_main_file(open_main_file())
    create_updated_file()
    for host in hosts:
        update_hosts(hostname=host[0], username=host[1], password=host[2])


if __name__ == "__main__":
    main()
