import unittest
import omailer

class ContactsIndexMock:
    def __init__(self):
        self.emails = ['1.a@p.com', '2.a@p.com', '3.a@p.com', '4.a@p.com', '5.a@p.com', '6.a@p.com',
                         '1.b@p.com', '2.b@p.com', '3.b@p.com', '4.b@p.com', '5.b@p.com', '6.b@p.com',
                         '1.c@p.com', '2.c@p.com', '3.c@p.com', '4.c@p.com', '5.c@p.com', '6.c@p.com']
        self.names = ['A, 1', 'A, 2', 'A, 3', 'A, 4', 'A, 5', 'A, 6',
                      'B, 1', 'B, 2', 'B, 3', 'B, 4', 'B, 5', 'B, 6',
                      'C, 1', 'C, 2', 'C, 3', 'C, 4', 'C, 5', 'C, 6']

    def total(self):
        return len(self.names)

    def name_at(self, i):
        return self.names[i].lower()

    def email_at(self, i):
        return self.emails[i]


class OmailerTest(unittest.TestCase):
    def test_contacts_are_received(self):
        contacts_index = omailer.get_all_contacts()
        self.assertTrue(contacts_index)
        self.assertGreater(contacts_index.total(), 0)

    def test_a_contact_index_is_found_startingwith(self):
        all_contacts = []
        contact_index_seed = omailer.find_a_contact_index_startswith(ContactsIndexMock(), 'c, 4')
        print('test contact is at ' + str(contact_index_seed))
        self.assertIsNotNone(contact_index_seed)


if __name__ == "__main__":
    unittest.main()
    