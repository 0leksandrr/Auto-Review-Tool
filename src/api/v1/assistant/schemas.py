from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field
from typing import List


class Product(BaseModel):
    url: HttpUrl
    description: str


class AssistantSchemaRequest(BaseModel):
    description: str = Field(..., min_length=10, max_length=500, description="Description of the customer's request.")
    links: List[Product] = Field(..., description="List of product links provided by the customer.")


class AssistantSchemaResponse(BaseModel):
    links: List[str] = Field(..., description="The list of product links.")
    timestamp: datetime = Field(..., description="The time when the response was created.")

    @classmethod
    def create(cls, links: List[str] = None) -> 'AssistantSchemaResponse':
        if links is None:
            links = []

        valid_links = [str(url) for url in links[0]]
        return cls(links=valid_links, timestamp=datetime.now())
