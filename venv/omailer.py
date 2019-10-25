import os
import win32com.client as win32


class ContactsIndex:
    def __init__(self, all_contacts, n_contacts):
        self.all_contacts = all_contacts
        self.n_contacts = n_contacts

    def total(self):
        return self.n_contacts

    def name_at(self, i):
        return str(self.all_contacts[i]).lower()

    def email_at(self, i):
        return self.all_contacts[i].GetExchangeUser().PrimarySmtpAddress.lower()

    def manager_name_at(self, i):
        return str(self.all_contacts[i].Manager)


def send_notification(mail_content):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = mail_content['to']
    mail.Cc = mail_content['cc']
    mail.Subject = mail_content['subject']
    mail.HtmlBody = mail_content['body']
    attachment_list = []
    if 'attachments' in mail_content:
        attachment_list = mail_content['attachments']
    for attachment in attachment_list:
        attachment_path = os.path.realpath(attachment)
        mail.Attachments.Add(attachment_path)
    #mail.send
    mail.Save()


def find_a_contact_index_startswith(contacts_index, lastname_prefix):
    low_bound = 0
    high_bound = contacts_index.total() - 1
    MAX_ITERABLE = 3
    while high_bound - low_bound > MAX_ITERABLE:
        mid_point = (high_bound + low_bound) // 2
        name_at_mid = contacts_index.name_at(mid_point)
        print('\r' + name_at_mid, end='')
        if lastname_prefix > name_at_mid:
            low_bound = mid_point + 1
        elif lastname_prefix < name_at_mid:
            high_bound = mid_point - 1
        else:
            return mid_point
    for i in range(low_bound, high_bound + 1):
        if lastname_prefix == contacts_index.name_at(i):
            return i
    return None


def neighbour_range_with_same_name(contacts_index, i, lowcase_americaname):
    low_neighbour = i - 1
    while low_neighbour >= 0 and \
          contacts_index.name_at(low_neighbour).lower() == lowcase_americaname:
        low_neighbour -= 1
    low_neighbour += 1

    high_neighbour = i + 1
    while high_neighbour < contacts_index.total() and \
          contacts_index.name_at(high_neighbour).lower() == lowcase_americaname:
        high_neighbour += 1
    high_neighbour -= 1

    return low_neighbour, high_neighbour


def match_email(contacts_index, i, lowcase_americaname, email):
    matched_index = i
    low_neighbour, high_neighbour = \
        neighbour_range_with_same_name(contacts_index, i, lowcase_americaname)
    for neighbour_index in range(low_neighbour, high_neighbour):
        if contacts_index.email_at(neighbour_index) == email:
            matched_index = neighbour_index
    return matched_index


def get_all_contacts():
    outlook = win32.Dispatch('outlook.application')
    mapi = outlook.GetNamespace("MAPI")
    addresses = mapi.AddressLists.Item("Global Address List")
    return ContactsIndex(addresses.AddressEntries, addresses.AddressEntries.Count)


def find_manager_from_lowcase_americaname(contacts_index, lowcase_americaname, email):
    index_by_lastname = find_a_contact_index_startswith(contacts_index, lowcase_americaname)
    if index_by_lastname:
        index_by_email = match_email(contacts_index, index_by_lastname, lowcase_americaname, email)
        if index_by_email:
            return contacts_index.manager_name_at(index_by_email)
    return None

