#!/usr/bin/python3

import pytest

from brownie.network.account import Account
from brownie.network.event import EventDict
from brownie.convert import EthAddress
from brownie import Wei


def test_value(accounts):
    tx = accounts[0].transfer(accounts[1], "1 ether")
    assert type(tx.value) is Wei
    assert tx.value == 1000000000000000000


def test_sender_receiver(accounts):
    tx = accounts[0].transfer(accounts[1], "1 ether")
    assert type(tx.sender) is Account
    assert tx.sender == accounts[0]
    assert type(tx.receiver) is EthAddress
    assert tx.receiver == accounts[1].address


def test_receiver_contract(accounts, tester):
    tx = tester.doNothing({"from": accounts[0]})
    assert type(tx.receiver) is EthAddress
    assert tester == tx.receiver
    data = tester.revertStrings.encode_abi(5)
    tx = accounts[0].transfer(tester.address, 0, data=data)
    assert type(tx.receiver) is EthAddress
    assert tester == tx.receiver


def test_contract_address(accounts, tester):
    tx = accounts[0].transfer(accounts[1], "1 ether")
    assert tx.contract_address is None
    assert type(tester.tx.contract_address) is str
    assert tester.tx.contract_address == tester
    assert tester.tx.receiver is None


def test_input(accounts, tester):
    data = tester.revertStrings.encode_abi(5)
    tx = accounts[0].transfer(tester.address, 0, data=data)
    assert tx.input == data


def test_fn_name(accounts, tester):
    tx = tester.setNum(42, {"from": accounts[0]})
    assert tx.contract_name == "BrownieTester"
    assert tx.fn_name == "setNum"
    assert tx._full_name() == "BrownieTester.setNum"
    data = tester.setNum.encode_abi(13)
    tx = accounts[0].transfer(tester, 0, data=data)
    assert tx.contract_name == "BrownieTester"
    assert tx.fn_name == "setNum"
    assert tx._full_name() == "BrownieTester.setNum"


def test_return_value(accounts, tester):
    owner = tester.getTuple(accounts[0])
    assert owner == tester.getTuple.transact(accounts[0]).return_value
    data = tester.getTuple.encode_abi(accounts[0])
    assert owner == accounts[0].transfer(tester, 0, data=data).return_value


def test_modified_state(accounts, tester, console_mode):
    assert tester.tx.modified_state
    tx = tester.setNum(42, {"from": accounts[0]})
    assert tx.status == 1
    assert tx.modified_state
    tx = tester.revertStrings(0, {"from": accounts[2]})
    assert tx.status == 0
    assert not tx.modified_state
    tx = accounts[0].transfer(accounts[1], "1 ether")
    assert tx.status == 1
    assert not tx.modified_state


def test_revert_msg(evmtester, console_mode):
    tx = evmtester.revertStrings(0)
    assert tx.revert_msg == "zero"
    tx = evmtester.revertStrings(1)
    assert tx.revert_msg == "dev: one"
    tx = evmtester.revertStrings(2)
    assert tx.revert_msg == "two"
    tx = evmtester.revertStrings(3)
    assert tx.revert_msg == ""
    tx = evmtester.revertStrings(31337)
    assert tx.revert_msg == "dev: great job"


def test_revert_msg_via_jump(ext_tester, console_mode):
    tx = ext_tester.getCalled(2)
    assert tx.revert_msg == "dev: should jump to a revert"


def test_events(tester, console_mode):
    tx = tester.revertStrings(5)
    assert tx.status == 1
    assert type(tx.events) is EventDict
    assert "Debug" in tx.events
    tx = tester.revertStrings(0)
    assert tx.status == 0
    assert type(tx.events) is EventDict
    assert "Debug" in tx.events


def test_hash(tester):
    a = tester.doNothing()
    b = tester.doNothing()
    hash(a)
    assert a != b
    assert a == a


def test_attribute_error(tester):
    tx = tester.doNothing()
    with pytest.raises(AttributeError):
        tx.unknownthing
