# cflpr

Asynchronous Python client for the CFL Park&Ride mobile API. It handles authentication, token refresh, and helpers for fetching Park&Ride availability and ticket information.

## Installation

```bash
pip install cflpr
```

## Usage

```python
import asyncio
from cflpr.api import CFLPRAPI

def handle_refresh_token(token: str) -> None:
    print(f"New refresh token: {token}")

async def main() -> None:
    async with CFLPRAPI(refresh_token_listener=handle_refresh_token) as api:
        await api.authenticate("your-email@example.com", "your-password")
        tickets = await api.get_closed_tickets()
        for ticket in tickets:
            print(ticket)

if __name__ == "__main__":
    asyncio.run(main())
```

`CFLPRAPI` maintains the authenticated aiohttp session for you and refreshes access tokens automatically when they are about to expire. Attach a `refresh_token_listener` if you need to persist new refresh tokens.
