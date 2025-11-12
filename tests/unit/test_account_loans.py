from src.account import PersonalAccount

class TestLoans:

    def test_personal_loans(self):
        account = PersonalAccount("Alice", "Smith", "65012345678")
        account.transfer_in(100)
        account.transfer_in(150)
        account.transfer_in(200)
        assert account.submit_for_loan(500) == True
        assert account.balance == 950
        assert account.submit_for_loan(-500) == False
        assert account.balance == 950

        account2 = PersonalAccount("Bob", "Brown", "72012345678")
        account2.transfer_in(1000)
        account2.transfer_out(50)
        account2.transfer_in(30)
        account2.transfer_out(20)
        account2.transfer_in(10)
        assert account2.submit_for_loan(300) == True
        assert account2.balance == 1270

        account3 = PersonalAccount("Charlie", "Davis", "80012345678")
        account3.transfer_in(100)
        account3.transfer_out(50)
        assert account3.submit_for_loan(200) == False
        assert account3.balance == 50

        account4 = PersonalAccount("Diana", "Evans", "90012345678")
        account4.transfer_in(1000)
        account4.transfer_out(800)
        account4.transfer_in(20)
        account4.transfer_in(200)
        account4.transfer_out(100)
        account4.transfer_out(200)
        assert account4.submit_for_loan(400) == False

    def test_loan_condition(self):
        account = PersonalAccount("Alice", "Smith", "65012345678")
        account.transfer_in(100)
        account.transfer_in(150)
        account.transfer_in(200)
        assert account.are_last_three_income() == True

        account2 = PersonalAccount("Bob", "Brown", "72012345678")
        account2.transfer_in(100)
        account2.transfer_out(50)
        account2.transfer_in(30)
        account2.transfer_out(20)
        account2.transfer_in(10)
        assert account2.are_last_three_income() == False

        account3 = PersonalAccount("Charlie", "Davis", "80012345678")
        account3.transfer_in(100)
        account3.transfer_out(150)
        assert account3.are_last_three_income() == False
