import os
import json
import uuid
import plistlib
import spam_rules

class MailRules:
    '''
    MailRules - A helper for accessing, creating, and writing mail rules.
    '''
    def __init__(self, plist_path=None):
        username = os.getenv("USER")
        self.plist_path = f"/Users/{username}/Library/Mail/V9/MailData/SyncedRules.plist"
        try:
            with open(self.plist_path, "rb") as f:
                self.rule_data = plistlib.load(f, fmt=None, dict_type=dict)
        except:
            raise OSError(f"No Mail.app rules plist found at {self.plist_path}")

        self.rule_names = [rule["RuleName"] for rule in self.rule_data]
        self.ids = [rule["RuleId"] for rule in self.rule_data]

    def create_uuid(self):
        '''create_uuid - Creates a string of the UUID(1) spec, which matches macOS's version.
        '''
        return str(uuid.uuid1()).upper()


    def get_mail_rule_names(self) -> list:
        for rule in self.rule_data:
            rule_names = [rule["RuleName"] for rule in self.rule_data]
            return rule_names


    def get_mail_rule_detail(self, rule_name):
        for rule in self.rule_data:
            if rule["RuleName"] == rule_name:
                return rule


    def get_all_mail_rule_data(self) -> list:
        return json.dumps(self.rule_data)


    def create_rule(self, data=None):
        # Housekeeping.
        if not data or not isinstance(data, dict):
            raise exit("Argument 'data' was not defined or is not an instance of 'dict'.")

        ''' create_rule() - Create a mail rule and add it to the list of rules.
        
        Function under construction.
        
        Args:
            data - Must be a dict which contains valid fields for an Apple Mail rule.
        
        Rule Fields: (* denotes required)
            * AllCriteriaMustBeSatisfied  - boolean: Whether all rules must be satisfied
            * RuleName                    - str: Name of mail rule.
            * RuleId                      - str: UUID(1) unique identifier.
            * TimeStamp                   - int: Timestamp of when the rule was created 
                                                (not epoch?)
            * Criteria                    - list of dicts:)
                                            - * CriterionUniqueId: UUID(1) - Each criteria item
                                                appears to have its own UUID. 
                                            - Expression: str - string to match (e.g. email address)
                                            - Qualifier: str
                                                - BeginsWith | EndsWith | Contains | Equals
                                            - Header: str
                                                - From
                                                - To
                                                - Subject
                                                - Cc
                                                - AnyRecipient
                                                - AnyRecipientIncludesFullName
                                                - NoRecipientIncludesFullName
                                                - DateSent | DateReceived:
                                                    - DateIsRelative = true
                                                    - DateUnitType   = 0 
                                                    - Qualifier: IsLessThan | IsGreaterThan
                                                    - Expression: int (days)
                                                - Account: str (e.g. "imap://name%40of.email.account.com/")
                                                - SenderIsInAddressBook
                                                - SenderIsNotInAddressHistory
                                                - SenderIsMemberOfVIPSenders:
                                                    - Expression = "AllVIPSenders"
                                                - SenderIsMemberOfGroup | SenderIsNotMemberOfGroup:
                                                    - GroupName | Expression = str: name of group in Contacts.app
                                                    - GroupId = str (e.g. "<Host UUID>:ABGroup")
                                                - Body: 
                                                    - Expression: str - string found in message body
                                                - IsJunkMail
                                                - IsDigitallySigned
                                                - IsEncrypted
                                                - PriorityIsHigh | PriorityIsNormal | PriorityIsLow
                                                - AnyAttachment:
                                                    - Expression: str - string found in name of attachment
                                                - AttachmentType:
                                                    - Qualifier = IsEqualTo
                                                    - Expression: int
                                                        - 1  = Application
                                                        - 2  = Archive
                                                        - 3  = Document
                                                        - 4  = Executable
                                                        - 5  = Image
                                                        - 6  = Movie
                                                        - 7  = Music
                                                        - 8  = PDF
                                                        - 9  = Presentation
                                                        - 10 = Text
            MailboxURL                  - str: string of mailbox URL

        Actions: (Must use at least one)
            CopyToMailboxURL            - str: Name of mailbox URL
            MailboxURL                  - str: Name of mailbox URL
            Deletes                     - boolean: If true, deletes message.
            MarkRead                    - boolean
            NotifyUser                  - boolean
            SendNotification            - boolean: Sends notification to macOS user

            ShouldCopyMessage           - boolean: true copies message (must use with "CopyToMailboxURL")
            CopyToMailboxURL            - str: string to mailbox URL to copy message

            AutoResponseType            - int: Choices between 1-3
                                            - 1 = Forward message
                                            - 2 = Reply to message 
                                            - 3 = Redirect message
            ForwardRecipients           - list: list of email addresses to forward message (must use with "ResponseMessage")
            RedirectRecipients          - list: list of email addresses to redirect email (must use with "ResponseMessage")
            ResponseMessage             - str: Message to respond with. Will recognize '\n' characters.

            ShouldTransferMessage       - boolean
            StopEvaluatingRules         - boolean
            AppleScript                 - str: name of ".scpt" file in '~/Library/Application Scripts/com.apple.mail/'

            MarkFlagged                 - boolean: true, flags email with color (must use "FlagColor")
            FlagColor                   - int
                                        - Colors:
                                            - 0 = Red
                                            - 1 = Orange
                                            - 2 = Yellow
                                            - 3 = Green
                                            - 4 = Light Blue
                                            - 5 = Purple
                                            - 6 = Grey

            HighlightTextUsingColor     - boolean: 
                                            - true, highlights text MESSAGE color.
                                            - false, highlights text BACKGROUND color.
                                            - removing this field/key disables color effects.
            Color                       - int: number that represents color
                                        - Text:
                                            3503295  = deep blue
                                            6977676  = gray
                                            8674197  = purple
                                            14819865 = red
                                            16680485 = orange
                                            14134016 = yellow
                                            9485826  = green
                                        - Background:
                                            10209791 = light blue
                                            13235369 = light green
                                            16773531 = light yellow
                                            16763531 = light orange
                                            16750738 = light red
                                            14136549 = light purple
        '''
        # TODO: Need to write out all possible fields for writing a mail rule
        # and whether or not those values need to be filled out with a string,
        # int, list, bool, or dict. 

        if "RuleId" not in data:
            data["RuleId"] = self.create_uuid()
        
        self.rule_data.append(data)


    def write_rules(self, path=None):
        ''' write_rules() - Write the set of rules to the path of a plist file.
        
        Args: 
            path - (string) The full system path to the file to write the data.
        '''
        if not path:
            raise exit("Path not defined.")

        try:
            with open(path, "wb") as f:
                plistlib.dump(self.rule_data, f)
        except:
            raise OSError(f"Error writing data at path: {path}")
