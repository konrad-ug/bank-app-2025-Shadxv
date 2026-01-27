import pytest
from src.mongo_accounts_repository import MongoAccountsRepository
from src.account import PersonalAccount

def test_mongo_repository_unit(mocker):
    mock_collection = mocker.Mock()
    
    mock_client = mocker.Mock()
    mock_db = mocker.Mock()
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
