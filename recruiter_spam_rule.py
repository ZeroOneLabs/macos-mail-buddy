import os
from MacOSmailBuddy import MailRules
from MacOSmailBuddy.spam_rules import basic_spam_rule
username = os.getenv("USER")
'''
Recruiter Spam Rule - Stop spamming me with jobs that don't relate to me, recruiters!

This is a sample script I wrote with an idea to help collaborate on email sources
that are malicious or a nuisance. Feel free to collab on the spammer-domains.txt.

Use this with caution.

TODO: 
- Add a whois function to filter based on WHOIS info on the email domain?
- Could too many whois requests cause someone's IP to get flagged? 
'''
# Used this to test writing out plist data to my Desktop so I didn't
# accidentally write over existing mail rule data.
test_path = f"/Users/{username}/Desktop/test.plist"

mail_rules = MailRules()
rule_data = mail_rules.rule_data


new_spam_rule = basic_spam_rule

with open('spammer-domains.txt', 'r') as f:
    domains = f.read().split('\n')

for domain in domains:
    uuid = mail_rules.create_uuid()
    
    # As someone who's browsed a lot of logging performance forums and read up on 
    # methods of matching strings, I decided to go with 'EndsWith' rather than
    # 'Contains' because I think Apple Mail might perform better.
    # Zero tests have been done to support this. ;)
    #
    # Of course, after this loop you could create your own list of specific email
    # addresses and do a 'for email in emails' loop to keep adding to this spammer list.
    new_spam_rule["Criteria"].append(
        {
            "CriterionUniqueId": uuid,
            "Expression": domain,
            "Header": "From",
            "Qualifier": "EndsWith",
        }
    )

new_spam_rule["RuleId"] = mail_rules.create_uuid()
# new_spam_rule["RuleName"] = "No more recruiter spam" # Or something else if you want.

mail_rules.create_rule(new_spam_rule)
mail_rules.write_rules(path=test_path)
