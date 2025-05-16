from pydantic import BaseModel


class QuoteMetadata(BaseModel):
    author: str
    quote: str


class StoicQuote(BaseModel):
    data: QuoteMetadata
