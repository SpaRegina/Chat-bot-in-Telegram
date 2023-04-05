import requests


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        url = f"https://api.currencyfreaks.com/latest?apikey={API_KEY}&symbols={quote}&base={base}"
        response = requests.get(url)
        if response.status_code != 200:
            raise APIException(f"������ ��� ��������� ����� �����: {response.status_code}")
        data = response.json()
        if "error" in data:
            raise APIException(f"������ ��� ��������� ����� �����: {data['error']['message']}")
        if quote not in data["rates"]:
            raise APIException(f"���� ������ '{quote}' �� ������")
        rate = data["rates"][quote]
        return round(rate * amount, 2)
