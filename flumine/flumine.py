import logging

from .baseflumine import BaseFlumine
from .event.event import EventType

logger = logging.getLogger(__name__)


class Flumine(BaseFlumine):
    def run(self) -> None:
        """
        Main run thread
        """
        with self:
            while True:
                event = self.handler_queue.get()
                if event == EventType.TERMINATOR:
                    break

                elif event.EVENT_TYPE == EventType.MARKET_CATALOGUE:
                    print(event)

                elif event.EVENT_TYPE == EventType.MARKET_BOOK:
                    self._process_market_books(event)

                elif event.EVENT_TYPE == EventType.CURRENT_ORDERS:
                    print(event)

                elif event.EVENT_TYPE == EventType.CLEARED_MARKETS:
                    print(event)

                elif event.EVENT_TYPE == EventType.CLEARED_ORDERS:
                    print(event)

                elif event.EVENT_TYPE == EventType.CLOSE_MARKET:
                    print(event)

                elif event.EVENT_TYPE == EventType.STRATEGY_RESET:
                    print(event)

                elif event.EVENT_TYPE == EventType.CUSTOM_EVENT:
                    print(event)

                elif event.EVENT_TYPE == EventType.NEW_DAY:
                    print(event)

                else:
                    logger.error("Unknown item in handler_queue: %s" % str(event))

    def __repr__(self) -> str:
        return "<Flumine>"

    def __str__(self) -> str:
        return "<Flumine [%s]>" % self.status
