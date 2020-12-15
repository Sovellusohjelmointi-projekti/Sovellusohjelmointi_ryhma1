import requests

class MailGunApi:
    API_URL = 'https://api.mailgun.net/v3/sandbox9be86adbecee46cb9cc4b6091e029175/messages'

    def __init__(self, domain, api_key):
        self.domain = domain
        self.key = api_key
        self.base_url = self.API_URL.format(self.domain)

    def send_email(self, to, subject, text, html=None):
        if not isinstance(to, (list, tuple)):
            to = [to, ]
            data = {
                'from': 'joona.paakkonen <no-reply@{}>'.format(self.domain),
                #'from': 'TUASreservations <no-reply@sandbox9be86adbecee46cb9cc4b6091e029175>'.format(self.domain),
                'to': to,
                'subject': subject,
                'text': text,
                'html': html
            }


        response = requests.post(url=self.base_url,
                                 auth=('api', self.key),
                                 data=data)
        return response

def send_simple_message():
    return requests.post(
        "sandbox9be86adbecee46cb9cc4b6091e029175.mailgun.org/messages",
        auth=("api", "3ec268486f6770bb4f8a9f147fa227b3-e5da0167-69e770d9"),
        data={"from": "Väsynyt käyttäjä <mailgun@sandbox9be86adbecee46cb9cc4b6091e029175.mailgun.org>",
                "to": ["bar@example.com", "MillaS@sandbox9be86adbecee46cb9cc4b6091e029175.mailgun.org"],
                "subject": "Lol apua",
                "text": "wörk plz mon"})
