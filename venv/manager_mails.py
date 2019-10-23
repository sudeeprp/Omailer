import os
import json
import excel2json
import omailer
import group_report
import mailframe


PROCESSED_MANAGER_MAP = r'processed\dummy_manager_map.json'
CASE2_GROUP_REPORTS_FILE = r'incoming\Bootcamp case2 rubric.xlsx'
FRESH_REPORTS_FILE = r'incoming\Case 1 Review_U.xlsx'
FRESH_EMAIL_TO_MANAGER_MAP = r'incoming\member email to manager map.xlsx'


def rows_to_dict_list(excel_filename):
    ws = excel2json.get_sheet(excel_filename)
    return excel2json.map_rows_in_sheet(ws)


def get_fresh_email_to_manager_email():
    fresh_email_to_manager_email = {}
    if os.path.isfile(FRESH_EMAIL_TO_MANAGER_MAP):
        fresh_manager_emails = rows_to_dict_list(FRESH_EMAIL_TO_MANAGER_MAP)
        for email_pair in fresh_manager_emails:
            fresh_email_to_manager_email[email_pair['member email'].lower()] = email_pair['manager email'].lower()
    return fresh_email_to_manager_email


def make_manager_map(contacts_index, mapped_rows):
    manager_to_team_map = {}
    fresh_email_to_manager_email = get_fresh_email_to_manager_email()
    for row in mapped_rows:
        fresh_name = row['employee name']
        fresh_email = row['email - primary work'].lower()
        fresh_americaname = row['americaname'].lower()
        if len(fresh_email_to_manager_email) > 0:
            manager_contact = fresh_email_to_manager_email[fresh_email]
            manager_americaname = f"{manager_contact}, {manager_contact.split('@')[0].split('.')[0]}"
        else:
            manager_americaname = omailer.find_manager_from_lowcase_americaname\
                                    (contacts_index, fresh_americaname, fresh_email)
            manager_contact = manager_americaname
        if manager_americaname not in manager_to_team_map:
            manager_to_team_map[manager_americaname] = {'manager_contact': manager_contact, 'team': []}
        manager_to_team_map[manager_americaname]['team']\
            .append({'fresh_email': fresh_email,
                     'fresh_name': fresh_name})
    return manager_to_team_map


def write_manager_map(contacts_index, mapped_rows):
    manager_map = make_manager_map(contacts_index, mapped_rows)
    with open(PROCESSED_MANAGER_MAP, 'w') as f:
        f.write(json.dumps(manager_map, indent=2))
    print('\nWrote {} managers'.format(len(manager_map)))


def read_manager_map():
    with open(PROCESSED_MANAGER_MAP, 'r') as f:
        return json.loads(f.read())


def create_manager_map(mapped_groups):
    contacts_index = omailer.get_all_contacts()
    print('Got {} contacts'.format(contacts_index.total()))
    write_manager_map(contacts_index, mapped_groups)


def mail_managers(mapped_groups):
    manager_map = read_manager_map()
    groups_report = group_report.make_groups_report(mapped_groups)

    mapped_fresh = rows_to_dict_list(FRESH_REPORTS_FILE)
    members_report = group_report.make_fresh_report(mapped_fresh)

    for manager in manager_map:
        mail = mailframe.frame_mail(manager.split(',')[-1].title(),
                                    manager_map[manager]['manager_contact'],
                                    manager_map[manager]['team'],
                                    groups_report, members_report)
        omailer.send_notification(mail)
        print(str(mail))
        print('---------------------------------------')


if __name__ == "__main__":
    groups = rows_to_dict_list(CASE2_GROUP_REPORTS_FILE)
    print(f'Got {len(groups)} rows from {CASE2_GROUP_REPORTS_FILE}')
    create_manager_map(groups)
    mail_managers(groups)
