import pytest
import requests
from src.account import FirmAccount # Dostosuj ścieżkę importu

class TestFirmAccountNIP:
    valid_nip = "8461627563"
    company_name = "Mafia Podlaska"

    def test_create_account_valid_nip(self, mocker):
        mock_get = mocker.patch('requests.get')
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": {
                "subject": {"statusVat": "Czynny"}
            }
        }

        konto = FirmAccount(self.company_name, self.valid_nip)
        assert konto.nip == self.valid_nip
        assert mock_get.call_count == 1

    def test_constructor_raises_error_when_nip_not_found(self, mocker):
        mock_get = mocker.patch('requests.get')
        mock_get.return_value.json.return_value = {
            "result": {"subject": None}
        }

        with pytest.raises(ValueError) as excinfo:
            FirmAccount(self.company_name, self.valid_nip)

        assert str(excinfo.value) == "Company not registered!!"

    def test_create_account_with_invalid_format_nip(self, mocker):
        spy = mocker.spy(requests, 'get')

        konto = FirmAccount(self.company_name, "12345")

        assert konto.nip == "Invalid"
        assert spy.call_count == 0
