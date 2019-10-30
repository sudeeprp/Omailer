

def email_to_name(email):
    return email.split('@')[0].split('.')[0].title()


def try_get(dict, key):
    key = key.lower()
    if key in dict:
        return dict[key]
    else:
        return ''


def frame_body(course_name, member_report):
    return f'''<html>
<style>
table {{border-collapse: collapse;}}
table, td, th {{font-family: "Calibri";border: 1px solid #aaa;padding: 8px;}}
</style>
<body style='font-family: "Calibri";'>Dear {email_to_name(try_get(member_report, 'manager'))},<br>
As per our training policy, assessment is mandatory to complete for technical learning programs.<br>
<br>
Below is the test result for your team member; please look at appropriate remediation if the participant has not cleared the test.<br>
<br>
<table>
<tr><th>Employee ID</th><td>{try_get(member_report, 'Employee ID')}</td></tr>
<tr><th>Participant</th><td>{try_get(member_report, 'Participant')}</td></tr>
<tr><th>Manager</th><td>{try_get(member_report, 'Manager')}</td></tr>
<tr><th>Result</th><td>{try_get(member_report, 'Result')}</td></tr>
<tr><th>Remarks</th><td>{try_get(member_report, 'Remarks')}</td></tr>
</table>
<br>
Thanks,<br>
<br>
Bnil Nath
<p style='color: Gray;'>Learning and Development Team</p>
</body></html>
'''



def frame_mail(course_name, member_report):
    mail = {'to': member_report['manager'],
            'cc': f"{try_get(member_report, 'Participant')}; agusty.rebekah@philips.com",
            'subject': f'Test Result: {course_name}',
            'body': frame_body(course_name, member_report),
           }
    return mail
