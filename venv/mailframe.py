import os
import subprocess
import rating_map as r


ATTACHMENT_LOCATION = r'output'


def team_bullet_list(team):
    bullet_list = '<ul>'
    for member in team:
        bullet_list += f"<li>{member['fresh_record']['name'].title()}</li>"
    bullet_list += '</ul>'
    return bullet_list


def frame_body(manager_name, team):
    return f'''<html><body style='font-family: "Verdana";'>Hi {manager_name},<br>
The bootcamp assessment reports are attached.
These assessments are focused on opportunities to build their skills further.<br>
Some assessments may not be evaluated due to their absence / exams. Other reasons, if any, are marked in the report.<br>
<br>
As part of the process, we will approach you post 90 days to understand:
<ul>
<li>Usefulness of the program</li>
<li>Do the participants need further interventions?</li>
<li>How the program can be improved for future batches</li>
</ul>
The following member(s) from your team completed the bootcamp recently:

{team_bullet_list(team)}

Please let us know any impressions, or if you need clarifications.<br>
<br>
Thank you,<br>
  L&D Team
</body></html>
'''


def indiv_rating_row(before, after):
    if after != before:
        after = '<b>' + after + '</b>'
    return f'''<td style="text-align:center">{before}</td><td style="text-align:center">{after}</td>'''


def make_html_for_member(record):
    return f'''
<html>
<style>
h1, h2, p, table {{font-family: "Verdana";font-size: 100%;}}
table {{border-collapse: collapse;}}
table, td, th {{border: 1px solid #aaa;padding: 8px;}}
</style>
<h1>{record['name']}</h1>
<p>e-mail: {record['participant philips email']}</p>
<br><h2>Participant Performance Track</h2>
<p>As part of the bootcamp, participants submitted assignments and worked in teams on case-studies.
In the second case study, participants exchanged their work to make improvements on another team's code.
This is {record['name'].split()[0].title()}'s team-assessment, done as per Philips Behaviors.
The Philips Behaviors have been tailored to the work they may perform as fresh engineers</p>
<table>
<tr>
<th>Customers first</th>
<td>{r.customer_first(record)}</td>
</tr>
<tr>
<th>Quality<br>Integrity always</th>
<td>{r.quality_integrity(record)}</td>
</tr>
<tr>
<th>Eager to improve</th>
<td>{r.improve_existing(record)}</td>
</tr>
<tr>
<th><p>Team up to win</p><p>Take ownership to deliver fast</p></th>
<td>{r.teamwork_ownership(record)}</td>
</tr>
</table>
<br><h2>Individual Performance Track</h2>
<p>Capabilities were assessed at the beginning of the program and towards the end as well. The scores are given below.</p>
<table>
<tr><th>Criteria</th><th>Mid-program assessment</th><th>Final assessment</th></tr>
<tr><th>Maintainability: Simplicity & Precision</th>
    <td>{r.message_mid(record, '1-maintainability')}</td>
    <td>{r.message_final(record, '2-code organization')}</td></tr>
<tr><th>Handling 'unhappy' scenarios</th>
    <td>{r.message_mid(record, '1-reliability')}</td>
    <td>{r.message_final(record, '2-reliability / error handling')}</td></tr>
<tr><th>Unit testing</th>
    <td>{r.message_mid(record, '1-dev.efficiency')}</td>
    <td>{r.message_final(record, '2-ci pipe')}</td></tr>'
</table>
<br><p>{r.optional_remark(record)}</p>
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


def frame_attachments(team):
    attachments = []
    for member in team:
        filename = filename_from_email(member['fresh_email'])
        reportfile_of_member = find_report(filename)
        if not reportfile_of_member:
            html = make_html_for_member(member['fresh_record'])
            reportfile_of_member = write_report(filename, html)
        else:
            print(f"NOT generating {reportfile_of_member} again")
        attachments.append(reportfile_of_member)
    return attachments


def frame_mail(manager_name, manager_contact, team):
    mail = {'to': manager_contact,
            'cc': 'sudeep.prasad@philips.com; agusty.rebekah@philips.com',
            'subject': 'Bootcamp assessment-summary for your team member(s)',
            'body': frame_body(manager_name, team),
            'attachments': frame_attachments(team)
           }
    return mail
