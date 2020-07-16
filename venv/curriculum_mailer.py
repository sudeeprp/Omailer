import sys
import omailer
import excel2json


def format_participants(participants):
    formatted_parti = "<ol>"
    for participant_name in participants:
        formatted_parti += '<li>' + participant_name + '</li>'
    return formatted_parti + '</ol>'


streams = {
    'S1-emb': {
        'description': 'explores C++ in an embedded context',
        'languages': ['C++'],
        'technologies': ['One of Windows or Linux']
    },
    'S2-app-desk': {
        'description': 'explores desktop-application development using Microsoft Technologies',
        'languages': ['C++', 'C#'],
        'technologies': ['WCF', 'WPF', '.net core']
    },
    'S2-app-web': {
        'description': 'explores web-application development using Microsoft Technologies',
        'languages': ['C#'],
        'technologies': ['.net core', 'Angular']
    },
    'S3-cloud': {
        'description': 'explores web- and app-development using Java',
        'languages': ['Java'],
        'technologies': ['Spring', 'Angular']
    }
}


def frame_mail(manager_email, greeting_name, participants, stream_name):
    mail = {'to': manager_email,
            'cc': 'sudeep.prasad@philips.com',
            'subject': f'Confirmation of bootcamp course-content',
            'body':
                f'''<body style='font-family: "Calibri";'>Hi {greeting_name},<br>
The following fresh engineers will be joining your team after the bootcamp:
{format_participants(participants)}
<p>This mail is to confirm their course-contents and technology exposure.</p>

<p>We intend to include them in the stream called
<a href="https://forms.microsoft.com/Pages/ResponsePage.aspx?id=LXpAGnV2F02GkrOsKFMG5MIBykE8w1FAqEb47Plu6GVURDJUVkpMSkxERVhOTEo1ODU3SkdCTzQ1RS4u">
<b>{stream_name}</b>
</a>,
which {streams[stream_name]['description']} - gaining a broader outlook
than the immediate technology they would use.</p>

<p>The bootcamp aims to bring <i>Engineering Discipline</i> and <i>Philips Behaviors</i>:
Deliver quality with Clean & proven code, Unearth boundaries, Test-first,
Take ownership to Improve with Teamwork.</p>

<p>These behaviors will be learnt by repeated implementation in specific technologies.
Participants will be ready to carry forward the same spirit in different technologies
they encounter in their career.<br>
To start with, it is good if they use the same technology that they encounter in the business.</p>

The above participants will work with the following in the bootcamp:
<ul>
<li>Languages: {', '.join(streams[stream_name]['languages'])}</li>
<li>Technologies: {', '.join(streams[stream_name]['technologies'])}</li>
</ul>
<p>In case of any discrepancy in the batch, language or technology, please respond in
<a href="https://forms.microsoft.com/Pages/ResponsePage.aspx?id=LXpAGnV2F02GkrOsKFMG5MIBykE8w1FAqEb47Plu6GVURDJUVkpMSkxERVhOTEo1ODU3SkdCTzQ1RS4u">this form</a>
</p>
<p>In case of any discrepancy in the participant list, please contact
<a href="mailto:namrata.aind@philips.com">Namrata Aind</a>
</p>

Bye,<br>
Bnil and Sudeep
'''
            }
    return mail


def filter_entries_with_email(entries):
    return [x for x in entries if 'email' in x]


def get_unique_manager_streams(stream_map):
    manager_streams_map = {}
    for stream_row in filter_entries_with_email(stream_map):
        if stream_row['email'] in manager_streams_map:
            manager_streams_map[stream_row['email']]['streams'].append(stream_row['stream'])
        else:
            manager_streams_map[stream_row['email']] = {
                'name': stream_row['name'],
                'streams': [stream_row['stream']]
            }
    return manager_streams_map


def get_participants(stream_map, manager_email, stream_name):
    participants = []
    for stream_row in filter_entries_with_email(stream_map):
        if stream_row['email'] == manager_email and stream_row['stream'] == stream_name:
            participants.append(stream_row['participant name'])
    if len(participants) == 0:
        print(f"WARNING: No participants for {manager_email} / {stream_name}!")
    return participants


def get_first_name(fullname):
    return fullname.split()[0].capitalize()


def mail_managers(stream_map):
    manager_streams_map = get_unique_manager_streams(stream_map)
    for manager_email in manager_streams_map:
        manager_name = manager_streams_map[manager_email]['name']
        for stream_name in manager_streams_map[manager_email]['streams']:
            participants = get_participants(stream_map, manager_email, stream_name)
            greeting_name = get_first_name(manager_name)
            mail = frame_mail(manager_email, greeting_name, participants, stream_name)
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
        stream_map = excel2json.rows_to_dict_list(excel_filename, sheet_index=0, heading_row=1)
        mail_managers(stream_map)
    else:
        print(f"Usage: python {sys.argv[0]} <excel path>")
