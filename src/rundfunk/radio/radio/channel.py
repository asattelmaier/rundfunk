from enum import Enum


class Channel(Enum):
    DEUTSCHLANDFUNK = 'https://st01.sslstream.dlf.de/dlf/01/128/mp3/stream.mp3?aggregator=web'
    DEUTSCHLANDFUNK_KULTUR = 'https://st02.sslstream.dlf.de/dlf/02/128/mp3/stream.mp3?aggregator=web'
    DEUTSCHLANDFUNK_NOVA = 'https://st03.sslstream.dlf.de/dlf/03/128/mp3/stream.mp3?aggregator=web'
    EMPTY = ''
