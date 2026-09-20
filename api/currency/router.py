from fastapi import APIRouter, status, HTTPException
from core.deps import SessionDep, RequireUser
from domain.currency.service import CurrencyService
from datetime import date
from domain.currency.exceptions import CurrencyNotFoundError, ExchangeRateNotFoundError
from domain.currency.dto import CurrencyDTO, ExchangeRateDTO


router = APIRouter(prefix='/currencies', tags=['currencies'])


@router.get('', dependencies=[RequireUser], response_model=list[CurrencyDTO])
async def get_all_currencies(
    session: SessionDep,
):
    service = CurrencyService(session)
    return await service.list_currencies()


@router.get('/{currency_code}', dependencies=[RequireUser], response_model=ExchangeRateDTO | None)
async def get_currency_latest_rate(
    currency_code: str,
    session: SessionDep
):
    service = CurrencyService(session)
    try:
        return await service.get_latest_rate(currency_code)
    except CurrencyNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Currency not found'
        )
    except ExchangeRateNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='ExchangeRate not found'
        )


@router.get('/{currency_code}/history', dependencies=[RequireUser], response_model=list[ExchangeRateDTO])
async def get_currency_rate_history(
    currency_code: str,
    startdate: date,
    enddate: date,
    session: SessionDep
):
    service = CurrencyService(session)
    try:
        return await service.get_rate_history(currency_code, startdate, enddate)
    except CurrencyNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Currency not found'
        )


@router.get('/{currency_code}/all', dependencies=[RequireUser], response_model=list[ExchangeRateDTO])
async def get_all_currency_rate_history(
    currency_code: str,
    session: SessionDep
):
    service = CurrencyService(session)
    try:
        return await service.get_rates_for_currency(currency_code)
    except CurrencyNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Currency not found'
        )