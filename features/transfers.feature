Feature: Money Transfers
  As a bank customer
  I want to transfer money
  So that I can manage my funds

  Scenario: Incoming transfer
    Given an account with balance 100
    When I receive a transfer of 50
    Then the account balance should be 150

  Scenario: Outgoing transfer
    Given an account with balance 200
    When I send a transfer of 50
    Then the account balance should be 150

  Scenario: Outgoing transfer with insufficient funds
    Given an account with balance 50
    When I try to send a transfer of 100
    Then the transfer should fail
    And the account balance should remain 50

  Scenario: Express transfer
    Given an account with balance 100
    When I make an express transfer of 50
    Then the account balance should be 49