import requests


class CovalentClient:
    CHAIN_ID_MAP = {"bsc": "56"}

    @classmethod
    def get_transactions(
        cls,
        api_key: str,
        chain: str,
        address: str,
        page_number: int = 0,
        page_size: int = 100,
    ) -> list:
        headers = {
            "Content-Type": "application/json",
        }

        params = {
            "page-number": str(page_number),
            "page-size": str(page_size),
            "no-logs": "true",
        }

        chain_number = cls.CHAIN_ID_MAP[chain]

        response = requests.get(
            f"https://api.covalenthq.com/v1/{chain_number}/address/{address}/transactions_v2/",
            params=params,
            headers=headers,
            auth=(api_key, ""),
        )
        return response.json()["data"]["items"]
