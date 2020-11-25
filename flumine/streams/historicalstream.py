import logging
import datetime
from betfairlightweight.streaming import StreamListener, HistoricalGeneratorStream
from betfairlightweight.streaming.stream import BaseStream as BFLWBaseStream
from betfairlightweight.resources.baseresource import BaseResource

from .basestream import BaseStream

logger = logging.getLogger(__name__)


class Stream(BFLWBaseStream):
    """
    Custom bflw stream to speed up processing
    by limiting to inplay/not inplay or limited
    seconds to start.
    """

    _lookup = "mc"

    def snap(self, market_ids: list = None) -> list:
        market_books = []
        for cache in list(self._caches.values()):
            if market_ids and cache.market_id not in market_ids:
                continue
            # if market has closed send regardless
            if cache.market_definition["status"] != "CLOSED":
                if self._listener.inplay:
                    if not cache.market_definition["inPlay"]:
                        continue
                elif self._listener.seconds_to_start:
                    _now = datetime.datetime.utcfromtimestamp(cache.publish_time / 1e3)
                    _market_time = BaseResource.strip_datetime(
                        cache.market_definition["marketTime"]
                    )
                    seconds_to_start = (_market_time - _now).total_seconds()
                    if seconds_to_start > self._listener.seconds_to_start:
                        continue
                if self._listener.inplay is False:
                    if cache.market_definition["inPlay"]:
                        continue
            market_books.append(
                cache.create_resource(self.unique_id, self._lightweight, snap=True)
            )
        return market_books


class HistoricListener(StreamListener):
    """
    Custom listener to restrict processing by
    inplay or seconds_to_start.
    """

    def __init__(self, inplay: bool = None, seconds_to_start: float = None, **kwargs):
        super(HistoricListener, self).__init__(**kwargs)
        self.inplay = inplay
        self.seconds_to_start = seconds_to_start


class HistoricalStream(BaseStream):

    LISTENER = HistoricListener
    MAX_LATENCY = None

    def run(self) -> None:
        pass

    def handle_output(self) -> None:
        pass

    def create_generator(self):
        stream = HistoricalGeneratorStream(
            file_path=self.market_filter,
            listener=self._listener,
            operation=self.operation,
        )
        return stream.get_generator()
