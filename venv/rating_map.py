
def map_score(record, name_of_rating, ranges):
    if name_of_rating not in record:
        return 'Not evaluated'
    return map_message(record[name_of_rating], ranges)

def map_message(rating_str, ranges):
    rating = int(rating_str)
    for rate_range in ranges:
        if rating <= rate_range['upto']:
            return rate_range["msg"]
    raise Exception(f"invalid rate {rating_str}")

def upto(upper, message):
    return {"upto": upper, "msg": message}

def customer_first(record):
    return map_score(
        record, '2-customer first',
        [upto(4, '<b>Present</b>: Needs to practice customer-focus.<br><b>Next step</b>: Start questioning the purpose of the code.'),
         upto(6, '<b>Present</b>: Has sensitivity to customer-needs.<br><b>Next step</b>: Start on marketing material of your product.'),
         upto(8, '<b>Present</b>: Strives to get familiar with customer-related terminology.<br><b>Next step</b>: Broaden by exploring competition and industry sites.'),
         upto(10, '<b>Present</b>: Excellent customer-focus.<br><b>Next step</b>: Challenge by interfacing with stakeholders.')]
    )

def quality_integrity(record):
    if '1-dev.efficiency' not in record or '2-ci pipe' not in record:
        return "Not evaluated"
    rating_avg = (int(record['1-dev.efficiency']) + int(record['2-ci pipe'])) / 2
    return map_message(
        rating_avg,
        [upto(4, '<b>Present</b>: Needs to practice techniques to bring developer efficiency.<br><b>Next step</b>: Start getting familiar with CI pipes and micro-automation.'),
         upto(6, '<b>Present</b>: Has attempted automated tests and Continuous Integration.<br><b>Next step</b>: Start looking for ways to enhance error-handling.'),
         upto(8, '<b>Present</b>: Strives to enhance reliability and believes in automation.<br><b>Next step</b>: Involve in improving practices around you.'),
         upto(10, '<b>Present</b>: Proficient in usage of tools and Continuous Integration.<br><b>Next step</b>: Challenge with real-world problems.')]
    )

def improve_existing(record):
    if '2-reliability / error handling' not in record or '2-code organization' not in record:
        return "Not evaluated"
    rating_avg =\
        (int(record['2-reliability / error handling']) + int(record['2-code organization'])) / 2
    return map_message(
        rating_avg,
        [upto(4, '<b>Present</b>: Needs to practice improving existing code.<br><b>Next step</b>: Review instances where legacy improvements can be made.'),
         upto(6, '<b>Present</b>: Has appreciation for old code and recognizes improvements.<br><b>Next step</b>: Assign tasks that need legacy-code-improvements.'),
         upto(8, '<b>Present</b>: Strives to improve legacy and organizes well.<br><b>Next step</b>: Look for improvement opportunities in production code.'),
         upto(10, '<b>Present</b>: Has demonstrated boy-scout rule with efficient organization.<br><b>Next step</b>: Challenge with business-problem related to legacy code.')]
    )

def teamwork_ownership(record):
    return map_score(
        record, '2-teamwork & ownership',
        [upto(6, '<b>Present</b>: Needs to practice working in teams.<br><b>Next step</b>: Initiate conversations with team-members.'),
         upto(8, '<b>Present</b>: Has demonstrated good teamwork.<br><b>Next step</b>: Initiate conversations with seniors.'),
         upto(10, '<b>Present</b>: Strives to excel and appreciates team-mates.<br><b>Next step</b>: Challenge with tasks that require stakeholder-buy-in.')]
    )

def score_to_practice(stage_of_bootcamp, record, name_of_rating):
    if name_of_rating not in record:
        return "Not evaluated"
    return stage_of_bootcamp + ":<br>" + map_message(
        record[name_of_rating],
        [upto(3, 'Getting started'),
         upto(6, 'Initial practice'),
         upto(8, 'Standard practice'),
         upto(10, 'Advanced practice')]
    )

def message_mid(record, name_of_rating):
    return score_to_practice("Own code", record, name_of_rating)

def message_final(record, name_of_rating):
    return score_to_practice("Legacy with dependencies", record, name_of_rating)

def optional_remark(record):
    if 'remarks' in record:
        return '<b>Additional Remarks</b>: ' + record['remarks']
    else:
        return ""
