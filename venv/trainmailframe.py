

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
table, td, th {{font-family: "Verdana";border: 1px solid #aaa;padding: 8px;}}
</style>
<body style='font-family: "Verdana";'>Dear {email_to_name(try_get(member_report, 'manager'))},<br>
As per our training policy, assessment is mandatory to complete for technical learning programs.<br>
<br>
Below is the test result for your team member; please look at appropriate remediation if the participant has not cleared the test.<br>
<br>
Program Name: {course_name}
<br>
<table>
<tr><th>Employee ID</th><td>{try_get(member_report, 'Employee ID')}</td></tr>
<tr><th>Participant</th><td>{try_get(member_report, 'Participant')}</td></tr>
<tr><th>Manager</th><td>{try_get(member_report, 'Manager')}</td></tr>
<tr><th>Result</th><td>{try_get(member_report, 'Result')}</td></tr>
<tr><th>Remarks</th><td>{try_get(member_report, 'Remarks')}</td></tr>
</table>
<br>
Thank you,<br>
  L&D Team
</body></html>
'''



def frame_mail(course_name, member_report):
    mail = {'to': member_report['manager'],
            'cc': 'sudeep.prasad@philips.com; agusty.rebekah@philips.com',
            'subject': course_name,
            'body': frame_body(course_name, member_report),
           }
    return mail
