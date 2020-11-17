import os
import json
import excel2json
import omailer
import mailframe


PROCESSED_MANAGER_MAP_TIDY = os.path.join('processed', 'manager_map.json')
PARTICIPANTS_REPORT_FILE = os.path.join('incoming', 'feedback-2020.xlsx')


def select_for_feedback(rows):
    return [r for r in rows if
            'participant philips email' in r and
            'joining team manager email' in r]


def make_manager_map(mapped_rows):
    manager_to_team_map = {}
    rows_to_feedback = select_for_feedback(mapped_rows)
    for row in rows_to_feedback:
        fresh_email = row['participant philips email'].lower()
        manager_contact = row['joining team manager email']
        if manager_contact not in manager_to_team_map:
            manager_to_team_map[manager_contact] = \
                {'manager_name': row['joining team manager'], 'team': []}
        manager_to_team_map[manager_contact]['team']\
            .append({'fresh_email': fresh_email,
                     'fresh_record': row})
    return manager_to_team_map


def write_manager_map(mapped_rows):
    manager_map = make_manager_map(mapped_rows)
    with open(PROCESSED_MANAGER_MAP_TIDY, 'w') as f:
        f.write(json.dumps(manager_map, indent=2))
    print('\nWrote {} managers'.format(len(manager_map)))


def mail_managers(manager_map_filename):
    with open(manager_map_filename, 'r') as manager_map_file:
        manager_contact_to_records = json.loads(manager_map_file.read())
        for manager_contact in manager_contact_to_records:
            record = manager_contact_to_records[manager_contact]
            mail = mailframe.frame_mail(record['manager_name'].split()[0].title(),
                                        manager_contact,
                                        record['team'])
            omailer.send_notification(mail)
            print(f"Sent to {record['manager_name']}")
            print('---------------------------------------')


if __name__ == "__main__":
    participants = excel2json.rows_to_dict_list(PARTICIPANTS_REPORT_FILE)
    print(f'Got {len(participants)} rows from {PARTICIPANTS_REPORT_FILE}')
    write_manager_map(participants)
    mail_managers(PROCESSED_MANAGER_MAP_TIDY)
