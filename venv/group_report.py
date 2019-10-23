

def make_groups_report(mapped_rows):
    current_batch = ''
    current_group = ''
    current_batch_report = {'members': []}
    groups_report = []
    for row in mapped_rows:
        if row['batch'] == current_batch and row['group'] == current_group:
            current_batch_report['members'].append(row['email - primary work'].lower())
        else:
            groups_report.append(current_batch_report)
            current_batch_report = {'members': []}
            current_batch = row['batch']
            current_group = row['group']
            current_batch_report['batch'] = current_batch
            current_batch_report['group'] = current_group
            current_batch_report['members'].append(row['email - primary work'].lower())
            current_batch_report['cust_first'] = row['Prod & Q goals:\nCustomer first'.lower()]
            current_batch_report['q_always'] = row['M & Refactoring:\nQuality Always'.lower()]
            current_batch_report['team_own'] = row['Team & Own'.lower()]
            current_batch_report['api_test'] = row['API test'.lower()]
            current_batch_report['unit_tests'] = row['Unit tests'.lower()]
            current_batch_report['automation'] = row['Automation'.lower()]
    groups_report.append(current_batch_report)
    return groups_report


def make_fresh_report(mapped_rows):
    freshers_report = []
    for row in mapped_rows:
        fresh_report = {}
        fresh_report['email'] = row['Email - Primary Work'.lower()].lower()
        fresh_report['clarity'] = row['Clarity of thought and expression'.lower()]
        fresh_report['business_understanding'] = \
            row['Business Understanding from problem statement'.lower()]
        fresh_report['q_response'] = row['Query Response'.lower()]
        fresh_report['body_lang'] = row['Body Language'.lower()]
        fresh_report['team_play'] = row['Team Player'.lower()]
        fresh_report['confidence'] = row['Confidence'.lower()]
        fresh_report['util_mentor'] = row['Utilization of mentor for learning'.lower()]
        if 'remark' in row:
            fresh_report['remark'] = row['remark']
        freshers_report.append(fresh_report)
    return freshers_report
