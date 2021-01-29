
def get_email_name(email):
    names = email[0:email.find('@')].split('.')
    if len(names) > 1:
        return (names[0], ' '.join(names[1:]))
    return (names[0], '')
