import smtplib
from enum import Enum


class Carriers(Enum):
    ATT = "@mms.att.net"
    TMOBILE = "@tmomail.net"
    VERIZON = "@vtext.com"
    SPRINT = "@messaging.sprintpcs.com"

    @property
    def domain(self):
        return self.value


class Texter:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.smtp_server = None
        self._create_smtp_server()

    def _build_recipient_address(self, phone_number: str, carrier: Carriers):
        recipient = phone_number + carrier.domain
        return recipient

    def _create_smtp_server(self):
        self.smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        self.smtp_server.starttls()
        self.smtp_server.login(self.email, self.password)

    def send_message(self, phone_number: str, carrier: Carriers, message: str):
        """
        Takes a number without international calling code.

        :param phone_number:
        :param carrier:
        :param message:
        :return:
        """
        recipient = self._build_recipient_address(phone_number, carrier)
        self.smtp_server.sendmail(self.email, recipient, message)


if __name__ == "__main__":
    texter = Texter("tinderfacebook91@gmail.com", "vutran-8vihxe-qikruK")
    texter.send_message("2173082840", Carriers.ATT, "you're gay")
