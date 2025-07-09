from enum import Enum


class StatusEnum(str, Enum):
    open = 'open'
    closed = 'closed'


class SentimentEnum(str, Enum):
    positive = 'positive'
    negative = 'negative'
    neutral = 'neutral'
    unknown = 'unknown'


class CategoryEnum(str, Enum):
    technical = 'техническая'
    payment = 'оплата'
    other = 'другое'
