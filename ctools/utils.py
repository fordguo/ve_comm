
def get_email_name(email):
    names = email[0:email.find('@')].split('.')
    if len(names) > 1:
        return (names[0], ' '.join(names[1:]))
    return (names[0], '')


def isascii(s):
    """Check if the characters in string s are in ASCII, U+0-U+7F."""
    return len(s) == len(s.encode())
