import main


def test_class():
    auth_file = open('authorized_keys_test', 'r')
    auth_test = auth_file.readline()
    main.sync_auth_keys_with_main_file('authorized_keys_test', 'test_main_file')
    main_file = open('test_main_file', 'r')
    main_test = main_file.readline()
    print(main_test + "\n" + auth_test)
    assert main_test == auth_test


def test_compare_lines():
    line_file = open('authorized_keys_test', 'r')
    line = line_file.readline()
    main_file = open('test_main_file', 'r')
    main_test = main_file.readline()
    check = main.compare_line_to_file(line_file, main_test)
    assert check == True


# def check_sync():
#     main.get_authorized_keys('192.168.16.172', username='mmd', password='Mmd.123!')
#     main.sync_auth_keys_with_main_file(main.open_main_file())
#     main.create_updated_file()
#     main.update_hosts('192.168.16.172', username='mmd', password='Mmd.123!')
#     main_file = open('main_file_for_keys', 'r')
#     main_test = main_file.readlines()
#     assert main.get_authorized_keys('192.168.16.172', username='mmd', password='Mmd.123!') == main_test
#






    #given = exitsting key file and main
    #when = readlinebyline
    #then = write to file
