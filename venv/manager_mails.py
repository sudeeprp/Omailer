import json
import excel2json
import omailer
import group_report
import mailframe


PROCESSED_MANAGER_MAP = r'processed\dummy_manager_map.json'
CASE2_GROUP_REPORTS_FILE = r'incoming\Bootcamp case2 rubric.xlsx'
FRESH_REPORTS_FILE = r'incoming\Case 1 Review_U.xlsx'


def rows_to_dict_list(excel_filename):
    ws = excel2json.get_sheet(excel_filename)
    return excel2json.map_rows_in_sheet(ws)


def make_manager_map(contacts_index, mapped_rows):
    fresh_email_to_manager_map = {}
    for row in mapped_rows:
        fresh_name = row['employee name']
        fresh_email = row['email - primary work'].lower()
        fresh_americaname = row['americaname'].lower()
        manager_americaname = omailer.find_manager_from_lowcase_americaname\
                                (contacts_index, fresh_americaname, fresh_email)
        if manager_americaname not in fresh_email_to_manager_map:
            fresh_email_to_manager_map[manager_americaname] = []
        fresh_email_to_manager_map[manager_americaname]\
            .append({'fresh_email': fresh_email,
                     'fresh_name': fresh_name})
    return fresh_email_to_manager_map


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
        mail = mailframe.frame_mail(manager, manager_map[manager], groups_report, members_report)
        omailer.send_notification(mail)
        print(str(mail))
        print('---------------------------------------')


if __name__ == "__main__":
    groups = rows_to_dict_list(CASE2_GROUP_REPORTS_FILE)
    print(f'Got {len(groups)} rows from {CASE2_GROUP_REPORTS_FILE}')
    '''The manager map is cached. Uncomment this if you want to regenerate'''
    '''create_manager_map(groups)'''
    mail_managers(groups)
