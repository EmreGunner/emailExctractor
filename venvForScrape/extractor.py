import re
def extract_mails(html):
    pattern = r"[a-zA-Z0-9\.\-+_]+@[a-zA-Z0-9\.\-+_]+\.[a-z]+"
    #logging.info('%s got the content ',html)
    all_mails = re.findall(pattern, html)
    mails = []
    if not all_mails:
        print("No email found.")
        return "no-email-found"
    else:
        if(type(all_mails) is list):
            print("got mails as list")
            for mail in all_mails:
                print("MAIL :" ,mail)
                if mail not in mails: 
                    if(validate_email(mail)):
                        mails.append(mail)
        if(type(all_mails) is str):
            print("got mails as STR")
            print("MAIL :" ,mail)
            if mail not in mails: 
                    if(validate_email(mail)):
                        mails.append(mail)
        return list(set(mails))
 
def validate_email(email):
    #not_allowed_domain = ["wixpress.com"]
    if not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email):
        return False
    if email[0].isdigit():
        return False
    if  (email.endswith('.jpg') or email.endswith('.png') or email.endswith('.webp') or email.endswith('.gif') or  email.endswith('wixpress.com') or email.endswith('example.com') or email.endswith('godaddy.com') or email.endswith('domain.com')):
        return False
    return True
