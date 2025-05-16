from pydantic import BaseModel, field_validator
from urllib.parse import unquote


class RandomFox(BaseModel):
    image: str
    link: str

    @field_validator("image", "link", mode="before")
    @classmethod
    def clean_url(cls, value: str) -> str:
        # Decode URL-encoded characters and remove backslashes
        cleaned = unquote(value.replace("\\", ""))
        return cleaned
