import os
import subprocess
import rating_map


ATTACHMENT_LOCATION = r'output'


def team_bullet_list(team):
    bullet_list = '<ul>'
    for member in team:
        bullet_list += f"<li>{member['fresh_name'].title()}</li>"
    bullet_list += '</ul>'
    return bullet_list


def find_record(value, search_in, search_by):
    found_item = None
    found_list = [item for item in search_in if value in item[search_by]]
    if len(found_list) == 1:
        found_item = found_list[0]
    return found_item


def frame_body(manager_name, team, groups_report, members_report):
    return f'''<html><body style='font-family: "Verdana";'>Hi {manager_name},<br>
The following member(s) from your team completed the bootcamp recently:

{team_bullet_list(team)}

In this mail, the assessment made during the bootcamp is attached. The assessment was <i>formative</i>, which means it focused on future improvements.<br>
<br>
As a process, we will approach you post 90 days, to understand:
<ul>
<li>Usefulness of the program</li>
<li>Do the participants need further interventions?</li>
<li>How the program can be improved for future batches</li>
</ul>
Please let us know any impressions, or if you need clarifications.<br>
<br>
Thank you,<br>
Bye,<br>
  Bnil and Sudeep
</body></html>
'''


def make_html_for_member(member, groups_report, members_report):
    email = member['fresh_email']
    case_study_record = find_record(email, search_in=groups_report, search_by='members')
    individual_record = find_record(email, search_in=members_report, search_by='email')
    def group_rating(key):
        return rating_map.GROUP_ASSESSMENT_MAP[case_study_record[key]]
    def indiv_rating(key):
        return rating_map.INDIVIDUAL_ASSESSMENT_MAP[individual_record[key]]
    def optional_individual_remark(label, key):
        if key in individual_record:
            return f'{label}: {individual_record[key]}'
        return ''

    return f'''
<html>
<style>
h1, h2, p, table {{font-family: "Verdana";font-size: 100%;}}
table {{border-collapse: collapse;}}
table, td, th {{border: 1px solid #ddd;padding: 8px;}}
</style>
<h1>{member['fresh_name']}</h1>
<p>e-mail: {email}</p>
<br><h2>Group case-study</h2>
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
<br><h2>Individual Assessment</h2>
<p>The following scores are on a scale of 1 to 5, with 5 being the highest</p>
<table>
<tr><th>Clarity of thought and expression</th><td>{indiv_rating('clarity')}</td></tr>
<tr><th>Response to Queries</th><td>{indiv_rating('q_response')}</td></tr>
<tr><th>Team Player</th><td>{indiv_rating('team_play')}</td></tr>
<tr><th>Confidence</th><td>{indiv_rating('confidence')}</td></tr>
<tr><th>Utilization of mentor and experts</th><td>{indiv_rating('util_mentor')}</td></tr>
</table>
<br><p>{optional_individual_remark('Additional Remark', 'remark')}</p>
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


def frame_mail(manager_name, manager_contact, team, groups_report, members_report):
    mail = {'to': manager_contact,
            'cc': 'sudeep.prasad@philips.com; bnil.nath@philips.com',
            'subject': 'Bootcamp summary: Your reports',
            'body': frame_body(manager_name, team, groups_report, members_report),
            'attachments': frame_attachments(team, groups_report, members_report)
           }
    return mail
