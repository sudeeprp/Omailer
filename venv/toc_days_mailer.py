import sys
import omailer
import excel2json


def format_participants(participants):
    formatted_parti = "<ol>"
    for participant_name in participants:
        formatted_parti += '<li>' + participant_name + '</li>'
    return formatted_parti + '</ol>'


def row(col1, col2):
    cell_style = 'style="padding: 15px; border-bottom: 1px solid black;"'
    return f"<tr><td {cell_style}>{col1}</td><td {cell_style}>{col2}</td></tr>"


def html_bullets(points):
    return f'''<ul><li>{'</li><li>'.join(points)}</li></ul>'''


def html_table(rows_html):
    return f'''<table style="border-collapse: collapse; border: 1px solid black;">
{rows_html}</table>'''


toc_github_classprep = \
    row('GitHub classroom intro, sample assignment', '1 day setup + try-out')
toc_acceptance = \
    row('I will code. With acceptance', '1 day guided assignment')
toc_agile = \
    row('''Agility and Completeness''', 'half-day')
toc_progparadigms = \
    row(f'''Programming Paradigms and Lifecycles<br>
    {html_bullets([
        'Hotspots',
        'Object-oriented decomposition',
        'Functional data-flows'])}''',
    '4 days practice & try-outs')
toc_common_prep = \
    f"{toc_github_classprep}{toc_acceptance}{toc_agile}{toc_progparadigms}"

toc_cpp_modular = \
    row(f'''Modular C++<br>
    {html_bullets([
        'Multiple files, linker, loader, precompiled headers',
        'Types, classes, objects, strings, I/O',
        'Applying inheritance'])}''',
    '3 days practice & try-outs')

toc_cpp_effective_3d = \
    row(f'''Effective C++<br>
    {html_bullets([
        'Collections & STL',
        'Memory & smart pointers',
        'Exceptions',
        'Pitfalls'])}''',
    '3 days practice & try-outs')

toc_cpp_effective_2d = \
    row(f'''Effective C++<br>
    {html_bullets([
        'Collections & STL',
        'Exceptions'])}''',
    '2 days practice & try-outs')

toc_cs_modular = \
    row(f'''Modular C#<br>
    {html_bullets([
        'Multiple files, IL binaries, loader',
        'Types, classes, objects, strings, I/O',
        'Applying inheritance'])}''',
    '3 days practice & try-outs')

toc_effective_cs = \
    row(f'''Effective C#<br>
    {html_bullets([
        'Collections',
        'Memory and garbage collection',
        'Exceptions, Reflection'])}''',
    '3 days practice & try-out')

toc_java_modular = \
    row(f'''Modular Java<br>
    {html_bullets([
        'Multiple files, packages, loader',
        'Types, classes, objects, strings, I/O',
        'Applying inheritance'])}''',
    '3 days practice & try-outs')

toc_effective_java = \
    row(f'''Effective Java<br>
    {html_bullets([
        'Collections',
        'Memory and garbage collection',
        'Exceptions, Reflection'])}''',
    '3 days practice & try-outs')

toc_solid_classes = \
    row(f'''SOLID in classes<br>
    {html_bullets([
        'Single Responsibility',
        'Dependency Inversion'])}''',
    '2 days theory & practice')

toc_IDE_setup = \
    row(f'''Setup IDE for Quality-at-desk''', '2 day setup & refactor')

toc_data_serialization = \
    row(f'''Data Serialization for storage and communication''',
        '1 day theory & practice')

toc_data_base = \
    row(f'''Database review<br>
    {html_bullets([
        'Tables and SQL',
        'JSON storage'])}''',
    '1 day theory & practice')

toc_unit_tests = \
    row(f'''Unit tests<br>
    {html_bullets([
        'Selecting the smallest code and data',
        'Identifying & addressing risk',
        'Sharp asserts',
        'Test code smells'])}''',
    '1 day theory & practice')

toc_case1 = \
    row(f'''Case-1<br>
    {html_bullets([
        'Allocate teams and setup GitHub collaboration',
        'Setup code KPIs',
        'Test & Implementation cycles',
        'Mentor review',
        'Rework and Sign-off'])}''',
    '7 days team activity')

toc_os_nw = row(f'''OS and Networking basics<br>
    {html_bullets([
        'Networking, Programming with Sockets',
        'Wireshark, MQTT',
        'OS tooling for performance/resource tracking',
        'Threads, events, IPC'])}''',
    '5 days theory & practice')

toc_dotnetcore = row(f'''.net core<br>
    {html_bullets([
        '.net core middleware',
        'Building Web APIs'])}''',
    '2 days theory & practice')

toc_wcf = row(f'''WCF<br>
    {html_bullets([
        'Endpoints, Bindings, Contract',
        'Consuming Self-hosted services'])}''',
    '2 days theory & practice')

toc_wpf = row(f'''WPF<br>
    {html_bullets([
        'XAML properties and extensions',
        'Routing Events',
        'Resources and Data binding',
        'Model / View separation'])}''',
    '4 days theory & practice')

toc_jsts = row(f'''JavaScript and TypeScript<br>
    {html_bullets([
        'Browser/node introduction, functions',
        'Closure',
        'Types in JavaScript and TypeScript',
        'Dealing with JSON'])}''',
    '5 days theory & practice')

toc_python = row(f'''Python scripting<br>
    {html_bullets([
        'Python ecosystem',
        'Procedural scripting',
        'Basic automation'])}''',
    '3 days theory & practice')

toc_solid_framework = \
    row(f'''SOLID in frameworks<br>
    {html_bullets([
        'Open-close principle',
        'Interface segregation & Interface design'])}''',
    '2 days theory & practice')

toc_spring = \
    row(f'''Spring<br>
    {html_bullets([
        'Spring as Dependency Injection Container',
        'Springboot Web APIs',
        'Spring MVC and Data-access'])}''',
    '3 days theory & practice')

toc_angular = \
    row(f'''Angular<br>
    {html_bullets([
        'Angular Environment and CLI',
        'Modules, Components, Templates',
        'Services, Routing, Async operations'])}''',
    '3 days theory & practice')

toc_case2_dev = \
    row(f'''Case-2 development phase<br>
    {html_bullets([
        'Setup CI & CodeScene',
        'PoC with acceptance',
        'Tests',
        'Decomposition',
        'Test + implement, coverage, test report',
        'Review and close'])}''',
    '7 days team activity')

toc_case2_maintenance = \
    row(f'''Case-2 maintenance phase<br>
    {html_bullets([
        'Exchange and intake',
        'Enhancement tests',
        'Try-outs',
        'Test + enhance',
        'Test + enhance, coverage, test report',
        'Review and close'])}''',
    '7 days team activity')

stream_content = {
    'S1':
f'''This stream explores C++ in an embedded context<br>
{html_table(toc_common_prep + toc_cpp_modular + toc_solid_classes + toc_IDE_setup +
            toc_cpp_effective_3d + toc_data_serialization +
            toc_unit_tests + toc_case1 + toc_os_nw + toc_python + toc_solid_framework +
            toc_case2_dev + toc_case2_maintenance)}''',
    'S2.1':
f'''This stream explores desktop-application development using Microsoft Technologies<br>
{html_table(toc_common_prep + toc_cpp_modular + toc_solid_classes + toc_IDE_setup +
            toc_cpp_effective_2d + toc_cs_modular + toc_effective_cs + toc_data_base +
            toc_unit_tests + toc_case1 + toc_wcf + toc_dotnetcore + toc_wpf +
            toc_solid_framework + toc_python +
            toc_case2_dev + toc_case2_maintenance)}''',
    'S2.2':
f'''This stream explores web-application development using Microsoft Technologies<br>
{html_table(toc_common_prep + toc_cs_modular + toc_solid_classes + toc_IDE_setup +
            toc_effective_cs + toc_data_base + toc_dotnetcore +
            toc_unit_tests + toc_case1 + toc_jsts + toc_python + toc_solid_framework +
            toc_angular +
            toc_case2_dev + toc_case2_maintenance)}''',
    'S3':
f'''This stream explores web- and app-development using Java'<br>
{html_table(toc_common_prep + toc_java_modular + toc_solid_classes + toc_IDE_setup +
            toc_effective_java + toc_data_base +
            toc_unit_tests + toc_case1 + toc_jsts + toc_spring + toc_solid_framework +
            toc_python + toc_angular +
            toc_case2_dev + toc_case2_maintenance)}'''
}


def frame_mail(manager_email, greeting_name, participants, stream_name):
    mail = {'to': manager_email,
            'cc': 'bnil.nath@philips.com',
            'subject': f'Contents and Days of Bootcamp',
            'body':
                f'''<body style='font-family: "Calibri";'>Hi {greeting_name},<br>
<p>The bootcamp starts from August 13th (post onboarding and EoP)
and completes by the start of November. This mail contains details about the program.</p>
<p>The program aims to bring
Engineering Discipline and Philips Behaviors,
delivering quality with clean & proven code.</p>
<p>As you will see below, a lot of effort and detail goes into it.
We have two requests to enable full participation outcomes:</p>
<ul>
<li>We encourage BU interaction during the bootcamp. 
However, please ensure that the exercises and objectives of the bootcamp
are given higher priority. If they have other time-bound activities in parallel,
they cannot do justice to either.</li>
<li>Many objectives and exercises in the bootcamp will be stringent
(often more than the code encountered in legacy code-bases).
We will demand full adherence to them and encourage you to do so as well.</li>
</ul>

<p>Based on your inputs, the stream {stream_name} has been put together
for the following engineers:
{format_participants(participants)}

{stream_content[stream_name]}
<br>
Bye,<br>
Bnil and Sudeep
'''
            }
    return mail


def entries_with_email(entries):
    return [x for x in entries if 'email' in x]


def is_team_member(entry, manager_email, stream_name):
   return 'email' in entry\
        and entry['email'] == manager_email\
        and entry['stream'] == stream_name\
        and 'participant name' in entry


def stream_of_team(stream_map, manager_email, stream_name):
    return [row for row in stream_map if is_team_member(row, manager_email, stream_name)]


def get_unique_manager_streams(stream_map):
    manager_streams_map = {}
    for stream_row in entries_with_email(stream_map):
        if stream_row['email'] in manager_streams_map:
            manager_streams_map[stream_row['email']]['streams'].add(stream_row['stream'])
        else:
            manager_streams_map[stream_row['email']] = {
                'name': stream_row['hm in wd'],
                'streams': {stream_row['stream']}
            }
    return manager_streams_map


def get_participants(stream_map, manager_email, stream_name):
    participants = []
    for stream_row in stream_of_team(stream_map, manager_email, stream_name):
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
