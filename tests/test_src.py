import pytest

def test_index(client):
    response = client.get('/')
    assert b'Method of analysis' in response.data
    assert b'Period of performance' in response.data
    assert b'Stock' in response.data
    assert b'Submit' in response.data


def test_sma(client):
    response = client.post('/', data={'stock':'MSFT','method':'SMA','period':'ytd'})
    assert 'MSFT' in str(response.data)

def test_sma(client):
    response = client.post('/', data={'stock':'MSFT','method':'MACD','period':'ytd'})
    assert 'MSFT' in str(response.data)


def test_stock_not_informed(client):
    response = client.post('/', data={'stock':'','method':'SMA','period':'ytd'})
    assert 'Stock not informed' in str(response.data)


def test_long_weird_stock(client):
    response = client.post('/', data={'stock':'asffds','method':'SMA','period':'ytd'})
    assert 'Something went wrong' in str(response.data)


def test_invalid_criteria(client):
    response = client.post('/', data={'stock':'asds','method':'SMA','period':'ytd'})
    assert b'stock' in response.data
    

