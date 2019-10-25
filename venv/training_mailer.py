import os
import json
import excel2json
import omailer
import group_report
import mailframe


PROCESSED_MANAGER_MAP = r'processed\dummy_manager_map.json'
REPORTS_FILE = r'incoming\Bootcamp case2 rubric.xlsx'
FRESH_REPORTS_FILE = r'incoming\Case 1 Review_U.xlsx'
FRESH_EMAIL_TO_MANAGER_MAP = r'incoming\member email to manager map.xlsx'


def get_fresh_email_to_manager_email():
    fresh_email_to_manager_email = {}
    if os.path.isfile(FRESH_EMAIL_TO_MANAGER_MAP):
        fresh_manager_emails = excel2json.rows_to_dict_list(FRESH_EMAIL_TO_MANAGER_MAP)
        for email_pair in fresh_manager_emails:
            fresh_email_to_manager_email[email_pair['member email'].lower()] = email_pair['manager email'].lower()
    return fresh_email_to_manager_email


def make_manager_map(mapped_rows):
    manager_to_team_map = {}
    fresh_email_to_manager_email = get_fresh_email_to_manager_email()
    for row in mapped_rows:
        fresh_name = row['employee name']
        fresh_email = row['email - primary work'].lower()
        manager_contact = fresh_email_to_manager_email[fresh_email]
        manager_americaname = f"{manager_contact}, {manager_contact.split('@')[0].split('.')[0]}"
        if manager_americaname not in manager_to_team_map:
            manager_to_team_map[manager_americaname] = {'manager_contact': manager_contact, 'team': []}
        manager_to_team_map[manager_americaname]['team']\
            .append({'fresh_email': fresh_email,
                     'fresh_name': fresh_name})
    return manager_to_team_map


def mail_managers(manager_map, participants_map):
    mapped_fresh = excel2json.rows_to_dict_list(FRESH_REPORTS_FILE)
    members_report = group_report.make_fresh_report(mapped_fresh)

    for manager in manager_map:
        mail = mailframe.frame_mail(manager.split(',')[-1].title(),
                                    manager_map[manager]['manager_contact'],
                                    manager_map[manager]['team'],
                                    participants_map, members_report)
        omailer.send_notification(mail)
        print(str(mail))
        print('---------------------------------------')


if __name__ == "__main__":
    participants_map = excel2json.rows_to_dict_list(REPORTS_FILE, heading_row=2)
    manager_map = make_manager_map(participants_map)
    mail_managers(manager_map, participants_map)
