import unittest
from unittest import mock

from flumine.markets.markets import Markets
from flumine.markets.market import Market


class MarketsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.markets = Markets()

    def test_init(self):
        self.assertEqual(self.markets._markets, {})

    def test_add_market(self):
        mock_market = mock.Mock()
        self.markets.add_market("1.1", mock_market)
        self.assertEqual(self.markets._markets, {"1.1": mock_market})

    def test_add_market_reopen(self):
        mock_market = mock.Mock()
        self.markets._markets = {"1.1": mock_market}
        self.markets.add_market("1.1", mock_market)

        self.assertEqual(self.markets._markets, {"1.1": mock_market})
        mock_market.open_market.assert_called()

    def test_close_market(self):
        mock_market = mock.Mock()
        self.markets._markets = {"1.1": mock_market}
        self.markets.close_market("1.1")
        mock_market.close_market.assert_called()
        self.assertEqual(self.markets.markets, {})

    def test_markets(self):
        self.assertEqual(self.markets.markets, {})
        mock_market = mock.Mock()
        mock_market.closed = False
        mock_market_two = mock.Mock()
        mock_market_two.closed = True
        self.markets._markets = {"1.1": mock_market, "2.1": mock_market_two}
        self.assertEqual(self.markets.markets, {"1.1": mock_market})

    def test_iter(self):
        self.assertEqual(len([i for i in self.markets]), 0)

    def test_len(self):
        self.assertEqual(len(self.markets), 0)


class MarketTest(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_market_book = mock.Mock()
        self.market = Market("1.234", self.mock_market_book)

    def test_call(self):
        mock_market_book = mock.Mock()
        self.market(mock_market_book)

        self.assertEqual(self.market.market_book, mock_market_book)

    def test_init(self):
        self.assertEqual(self.market.market_id, "1.234")
        self.assertEqual(self.market.market_book, self.mock_market_book)
        self.assertFalse(self.market.closed)

    def test_open_market(self):
        self.market.open_market()
        self.assertFalse(self.market.closed)

    def test_close_market(self):
        self.market.close_market()
        self.assertTrue(self.market.closed)
