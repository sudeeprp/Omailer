import os
import subprocess
import rating_map


ATTACHMENT_LOCATION = r'output'


def team_bullet_list(team):
    bullet_list = ''
    for member in team:
        bullet_list += f". {member['fresh_name'].title()}\n"
    return bullet_list


def find_record(value, search_in, search_by):
    found_item = None
    found_list = [item for item in search_in if value in item[search_by]]
    if len(found_list) == 1:
        found_item = found_list[0]
    return found_item


def frame_body(manager, team, groups_report, members_report):
    return f'''Hi {manager.split(',')[-1]},
The following member(s) from your team completed the bootcamp recently:

{team_bullet_list(team)}

In this mail, the assessment made during the bootcamp is attached. The assessment was formative, which means it focused on future improvements.
We are interested in knowing your impressions of the engineers who have been through the bootcamp. 

Please let us know any impressions.

PS: This mail is sent based on the reporting structure in Outlook. 
If any of these engineers aren't reporting to you, please bring it to our notice.

Thank you,
Bye,
  Sudeep and Bnil
'''


def make_html_for_member(member, groups_report, members_report):
    email = member['fresh_email']
    case_study_record = find_record(email, search_in=groups_report, search_by='members')
    individual_record = find_record(email, search_in=members_report, search_by='email')
    def group_rating(key):
        return rating_map.GROUP_ASSESSMENT_MAP[case_study_record[key]]
    def indiv_rating(key):
        return rating_map.INDIVIDUAL_ASSESSMENT_MAP[individual_record[key]]
    return f'''
<html>
<style>
h1, h2, p, table {{font-family: "Verdana";font-size: 100%;}}
table {{border-collapse: collapse;}}
table, td, th {{border: 1px solid #ddd;padding: 8px;}}
</style>
<h1>{member['fresh_name']}</h1>
<p>e-mail: {email}</p>
<h2>Group case-study</h2>
<p>As part of the bootcamp, two case studies were done. 
In the second case study, participants exchanged their work to make improvements on another team's code.
This is {member['fresh_name'].split()[0].title()}'s team-assessment, done as per Philips Behaviors.</p>
<table>
<tr>
<th>Customers first</th>
<td>{group_rating('cust_first')}</td>
</tr>
<tr>
<th>Quality <span style="font-size: 70%">and Integrity always,</span>
<p>Eager to improve</p></th>
<td>{group_rating('q_always')}</td>
</tr>
<tr>
<th>Team up to win</th>
<td>{group_rating('team_own')}</td>
</tr>
<tr>
<th>Take ownership to deliver fast</th>
<td>{group_rating('unit_tests')}<br>{group_rating('automation')}</td>
</tr>
</table>
<h2>Individual Assessment</h2>
<p>The following scores are on a scale of 1 to 5, with 5 being the highest</p>
<table>
<tr><th>Clarity of thought and expression</th><td>{indiv_rating('clarity')}</td></tr>
<tr><th>Response to Queries</th><td>{indiv_rating('q_response')}</td></tr>
<tr><th>Team Player</th><td>{indiv_rating('team_play')}</td></tr>
<tr><th>Confidence</th><td>{indiv_rating('confidence')}</td></tr>
<tr><th>Utilization of mentor</th><td>{indiv_rating('util_mentor')}</td></tr>
</table>
</html>
    '''


def write_report(filename, html):
    html_filepath = os.path.join(ATTACHMENT_LOCATION, filename + '.html')
    with open(html_filepath, 'w') as f:
        f.write(html)
    pdf_filepath = os.path.join(ATTACHMENT_LOCATION, filename + '.pdf')
    subprocess.run(['wkhtmltopdf.exe', html_filepath, pdf_filepath])
    return pdf_filepath


def find_report(filename):
    file_found = None
    pdf_filepath = os.path.join(ATTACHMENT_LOCATION, filename + '.pdf')
    if os.path.isfile(pdf_filepath):
        file_found = pdf_filepath
    return file_found


def filename_from_email(email):
    return email.split('>')[-1].split('@')[0].replace('.', ' ')


def frame_attachments(team, groups_report, members_report):
    attachments = []
    for member in team:
        filename = filename_from_email(member['fresh_email'])
        reportfile_of_member = find_report(filename)
        if not reportfile_of_member:
            html = make_html_for_member(member, groups_report, members_report)
            reportfile_of_member = write_report(filename, html)
        else:
            print(f"NOT generating {reportfile_of_member} again")
        attachments.append(reportfile_of_member)
    return attachments


def frame_mail(manager, team, groups_report, members_report):
    mail = {'to': manager,
            'cc': 'sudeep.prasad@philips.com; bnil.nath@philips.com',
            'subject': 'Bootcamp summary: Your reports',
            'body': frame_body(manager, team, groups_report, members_report),
            'attachments': frame_attachments(team, groups_report, members_report)
           }
    return mail
