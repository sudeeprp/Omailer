import os
import sys
import excel2json
import omailer
import group_report
import trainmailframe


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


def mail_managers(course_name, participants_map):
    print(course_name)
    for participant in participants_map:
        mail = trainmailframe.frame_mail(course_name, participant)
        omailer.send_notification(mail)
        print(str(mail))
        print('---------------------------------------')


def get_course_name(excel_filename):
    ws = excel2json.get_sheet(excel_filename, sheet_number=1)
    course_name = ws['A1']
    return course_name


if __name__ == "__main__":
    if len(sys.argv) == 2:
        excel_filename = sys.argv[1]
        participants_map = excel2json.rows_to_dict_list(excel_filename, sheet_index=1, heading_row=2)
        mail_managers(get_course_name(excel_filename), participants_map)
    else:
        print(f"Usage: python {sys.argv[0]} <excel path>")
