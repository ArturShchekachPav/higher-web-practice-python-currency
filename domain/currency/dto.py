from datetime import date

from pydantic import BaseModel, ConfigDict


class CurrencyDTO(BaseModel):
    id: int
    code: str
    name: str
    nominal: int

    model_config = ConfigDict(from_attributes=True)


class ExchangeRateDTO(BaseModel):
    id: int
    currency_id: int
    rate: float
    date: date

    model_config = ConfigDict(from_attributes=True)