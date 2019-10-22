import omailer


def test_contact_integration(contacts_index):
    print('One name from integrated contacts: ' + contacts_index.name_at(100000))


def test_contact_search(contacts_index, americaname):
    i = omailer.find_a_contact_index_startswith(contacts_index, americaname)
    print('\n' + americaname + ' found at: ' + str(i))
    return i


def test_manager(contacts_index, americaname):
    i = omailer.find_a_contact_index_startswith(contacts_index, americaname)
    print('\n' + americaname + ' manager is: ' + contacts_index.manager_name_at(i))


def test_manager_from_email(contacts_index, email):
    print('\n' + email + ' manager is: ' + omailer.find_manager_from_email(contacts_index, email))


if __name__ == "__main__":
    contacts_index = omailer.get_all_contacts()
    test_contact_integration(contacts_index)
    test_contact_search(contacts_index, 'kumar, praveen')
    test_manager(contacts_index, 'prasad, sudeep')
    test_manager_from_email(contacts_index, 'sudeep.prasad@philips.com')
