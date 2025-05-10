__all__ = [
    "TokenNotSet",
    "MissingLLMProvider",
    "InvalidLLMProvider",
    "LangchainFailiure",
    "LCELFailiure",
    "ChainMissingInput",
    "ChainInputInvalid",
]


# Discord
class TokenNotSet(Exception):
    """Exception for Discord

    Raised when DISCORD_BOT_TOKEN cannot be read from environment variables
    """

    pass


# Custom
class MissingLLMProvider(Exception):
    """Custom Exception

    Raised when an LLM provider has not been set
    """


class InvalidLLMProvider(Exception):
    """Custom Exception

    Raised when an LLM provider is not recognized
    """


# Langchain
class LangchainFailiure(Exception):
    """Base Exception for Langchain

    Ideally speaking, this could be caught to handle any exceptions raised from langchain operations.
    """

    pass


class LCELFailiure(LangchainFailiure):
    """Base Exception for LCEL

    Exception that's raised when an operation related to LCEL (Langchain Expression Language) occurs
    """

    pass


class ChainMissingInput(LCELFailiure):
    """Exception that's raised when a chain is missing one/more inputs"""

    pass


class ChainInputInvalid(LCELFailiure):
    """Exception that's raised when a chain is given one/more invalid inputs"""

    pass
