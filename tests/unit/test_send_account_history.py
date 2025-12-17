import pytest
import datetime
from src.account import PersonalAccount, FirmAccount

class TestSendHistory:
    today_date = datetime.datetime.today().strftime("%Y-%m-%d")
    mail = "test@test.test"

    def test_pesonal_send_history(self, mocker):
        account = PersonalAccount("Thomas", "Smith", "12345678908")
        account.history = [100, -1, 500]
        mock_send = mocker.patch("lib.smtp.SMTPClient.send", return_value=True)

        result = account.send_history_via_email(self.mail)
        assert result is True
        mock_send.assert_called_once()
        subject = mock_send.call_args[0][0]
        text = mock_send.call_args[0][1]
        email_address = mock_send.call_args[0][2]
        assert subject == "Account Transfer History " + self.today_date
        assert text == "Personal account history: [100, -1, 500]"
        assert email_address == self.mail


    def test_firm_send_history(self, mocker):
        mock_get = mocker.patch('requests.get')
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": {
                "subject": {"statusVat": "Czynny"}
            }
        }

        account = FirmAccount("Some Company", "8461627563")
        account.history = [5000, -1000, 500]
        mock_send = mocker.patch("lib.smtp.SMTPClient.send", return_value=True)

        result = account.send_history_via_email(self.mail)
        assert result is True
        mock_send.assert_called_once()
        subject = mock_send.call_args[0][0]
        text = mock_send.call_args[0][1]
        email_address = mock_send.call_args[0][2]
        assert subject == "Account Transfer History " + self.today_date
        assert text == "Company account history: [5000, -1000, 500]"
        assert email_address == self.mail
