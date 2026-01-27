import pytest
from src.mongo_accounts_repository import MongoAccountsRepository
from src.account import PersonalAccount, FirmAccount

def test_mongo_repository_unit(mocker):
    mock_client = mocker.MagicMock()
    mock_db = mocker.MagicMock()
    
    mock_collection = mocker.Mock()

    mock_client.__getitem__.return_value = mock_db
    mock_db.__getitem__.return_value = mock_collection

    mocker.patch('src.mongo_accounts_repository.MongoClient', return_value=mock_client)
    
    repo = MongoAccountsRepository()
    
    account = PersonalAccount("Unit", "Test", "98765432109")
    account.balance = 100
    
    repo.save_all([account])
    mock_collection.delete_many.assert_called_once_with({})
    mock_collection.insert_one.assert_called_once()
    
    mock_collection.find.return_value = [account.to_dict()]

    loaded_accounts = repo.load_all()
    
    assert len(loaded_accounts) == 1
    assert loaded_accounts[0].pesel == "98765432109"
    assert loaded_accounts[0].balance == 100

def test_mongo_repository_load_firm_and_error(mocker):
    mock_collection = mocker.MagicMock()
    mock_db = mocker.MagicMock()
    mock_client = mocker.MagicMock()
    mock_client.__getitem__.return_value = mock_db
    mock_db.__getitem__.return_value = mock_collection

    mocker.patch('src.mongo_accounts_repository.MongoClient', return_value=mock_client)
    
    mock_validate_nip = mocker.patch('src.account.FirmAccount.validate_nip_via_mf')

    repo = MongoAccountsRepository()
    
    personal_acc_data = PersonalAccount("Jane", "Doe", "11223344556").to_dict()
    
    mock_validate_nip.return_value = True
    firm_acc_data_good = FirmAccount("Good Corp", "1234567890").to_dict()
    
    firm_acc_data_bad = FirmAccount("Bad Corp", "0987654321").to_dict()
    
    mock_collection.find.return_value = [personal_acc_data, firm_acc_data_good, firm_acc_data_bad]
    
    def side_effect(nip):
        if nip == "0987654321":
            raise ValueError("Invalid NIP")
        return True
    mock_validate_nip.side_effect = side_effect

    loaded_accounts = repo.load_all()

    assert len(loaded_accounts) == 2
    assert any(isinstance(acc, PersonalAccount) and acc.pesel == "11223344556" for acc in loaded_accounts)
    assert any(isinstance(acc, FirmAccount) and acc.company_name == "Good Corp" for acc in loaded_accounts)
    assert not any(isinstance(acc, FirmAccount) and acc.company_name == "Bad Corp" for acc in loaded_accounts)
