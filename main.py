import aiohttp
import asyncio
import sys
from datetime import datetime, timedelta

class PrivatBankAPI:
    def __init__(self):
        # Базовий URL для запитів до API ПриватБанку
        self.base_url = "https://api.privatbank.ua/p24api"

    async def fetch_exchange_rate(self, date: str):
        # Асинхронна функція для отримання курсу валют на певну дату
        async with aiohttp.ClientSession() as session:
            # Виконуємо GET-запит до API ПриватБанку, передаючи дату запиту
            async with session.get(f"{self.base_url}/exchange_rates?json&date={date}") as response:
                # Повертаємо результат у форматі JSON
                return await response.json()

    async def get_exchange_rates(self, days: int):
        # Метод для отримання курсу валют за останні декілька днів
        rates = []
        today = datetime.now()

        # Проходимося по кожному з днів, щоб отримати курс валют на кожен з них
        for i in range(days):
            # Формуємо дату для запиту, зменшуючи поточну дату на певну кількість днів
            date = (today - timedelta(days=i)).strftime('%d.%m.%Y')
            # Викликаємо асинхронну функцію fetch_exchange_rate для отримання курсу на певну дату
            data = await self.fetch_exchange_rate(date)
            # Форматуємо отримані дані та додаємо їх до списку курсів
            rates.append({date: {
                'EUR': {
                    'sale': data['exchangeRate'][0]['saleRateNB'],
                    'purchase': data['exchangeRate'][0]['purchaseRateNB']
                },
                'USD': {
                    'sale': data['exchangeRate'][19]['saleRateNB'],
                    'purchase': data['exchangeRate'][19]['purchaseRateNB']
                }
            }})
        return rates


async def main():
    # Перевіряємо чи користувач ввів вірну кількість аргументів
    if len(sys.argv) != 2:
        print("Usage: python main.py <number_of_days>")
        return

    try:
        # Зчитуємо кількість днів з аргументів командного рядка
        days = int(sys.argv[1])
    except ValueError:
        print("Number of days must be an integer")
        return

    # Перевіряємо, чи кількість днів не перевищує 10
    if days > 10:
        print("Number of days cannot exceed 10")
        return

    # Створюємо об'єкт класу PrivatBankAPI для взаємодії з API ПриватБанку
    api = PrivatBankAPI()
    # Отримуємо курс валют за вказану кількість днів
    exchange_rates = await api.get_exchange_rates(days)
    # Виводимо результат у вказаному форматі
    print(exchange_rates)

if __name__ == "__main__":
    # Викликаємо асинхронну функцію main() для запуску програми
    asyncio.run(main())