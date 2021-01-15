from post_office import mail
from post_office.connections import connections
from post_office.models import STATUS
import logging

logger = logging.getLogger(__name__)


def email_data(sender, email, subject, html):
    return {'sender': sender, 'recipients': [email], 'subject': subject, 'html_message': html}


def _check_conn():
    try:
        connections._connections.connections['default'].close()
        connections._connections.connections['default'].open()
    except AttributeError:
        pass


def send_mail(email_data):
    m = mail.send(**email_data)
    if m.status == STATUS.failed and m.logs.first().exception_type in ['SMTPServerDisconnected', 'SMTPRecipientsRefused']:
        logger.error(
            f'send mail failed with {m.logs.first().exception_type}. mail info:{email_data}')
        _check_conn()
        mail.send(**email_data)


def send_mail_now(email_data):
    email_data['priority'] = 'now'
    send_mail(email_data)
