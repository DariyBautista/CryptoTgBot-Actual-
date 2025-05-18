import aiohttp
from config import CMC_API_KEY
from typing import Optional

async def get_price_float(sym: str) -> Optional[float]:
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
    params = {"symbol": sym, "convert": "USD"}
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url, headers=headers, params=params) as r:
                if r.status != 200:
                    print(f"Error: API request failed with status {r.status}")
                    return None
                data = await r.json()
                return data["data"][sym]["quote"]["USD"]["price"]
    except KeyError:
        print(f"Error: Missing data for symbol {sym}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

