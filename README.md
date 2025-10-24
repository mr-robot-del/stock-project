# Stock Project API

Lightweight Django REST API for fetching, storing and exposing stock data and simple predictions. The project integrates with Alpha Vantage to populate daily time-series and provides endpoints to search stocks, view stock data, manage watchlists and portfolios.

## Key modules / references
- Settings & environment: [`core.settings.ALPHA_VANTAGE_API_KEY`](core/core/settings.py) — see [core/core/settings.py](core/core/settings.py)  
- Stock data fetcher: [`stocks.views.fetch_alpha_vantage_data`](core/stocks/views.py) — see [core/stocks/views.py](core/stocks/views.py)  
- Stock endpoints & logic: [`stocks.views.StockViewSet`](core/stocks/views.py) and [`stocks.views.StockDataViewSet`](core/stocks/views.py) — see [core/stocks/views.py](core/stocks/views.py)  
- Watchlist endpoints: [`users.views.WatchlistView`](core/users/views.py) — see [core/users/views.py](core/users/views.py)  
- Routes: [core/core/urls.py](core/core/urls.py), [core/stocks/urls.py](core/stocks/urls.py), [core/portfolios/urls.py](core/portfolios/urls.py)

## Features
- Search stocks via Alpha Vantage (SYMBOL_SEARCH)
- Fetch and cache daily stock time-series (auto-populates DB when missing)
- CRUD for stock data and simple prediction records
- User watchlist management
- Portfolio endpoints (list, details, add/remove stocks)

## Requirements
- Python 3.11+ (match your local environment)
- Dependencies defined in [requirements.txt](requirements.txt)

## Environment variables
Create a `.env` at the project root (the project already loads it from [core/core/settings.py](core/core/settings.py)). Required/optional keys:
- DJANGO_SECRET_KEY (required)
- ALPHA_VANTAGE_API_KEY (required to query Alpha Vantage) — used by [`core.settings.ALPHA_VANTAGE_API_KEY`](core/core/settings.py)
- DEBUG (optional, default False)
- ALLOWED_HOSTS (optional)

## Quick start (local)
1. Create venv and install deps
```bash
python -m venv venv
venv\Scripts\activate    # Windows
pip install -r 

Set environment variables (or create .env)
On Windows (PowerShell):
$env:DJANGO_SECRET_KEY = "replace-with-secret"
$env:ALPHA_VANTAGE_API_KEY = "your-alpha-vantage-key"

Migrate and create superuserpython  migrate
python  createsuperuser

Run server
python  runserver

Run tests
python  test

Main API endpoints
API root: as configured in core/core/urls.py
Stocks:
Search: GET /stocks/search/ (implemented by stocks.views.StockSearchView) — see core/stocks/urls.py
Stock data list/create: /stocks/stockdata/ (stocks.views.StockDataViewSet) — see core/stocks/urls.py
Stock-specific data: /stocks/<stock_pk>/stockdata/ — see core/stocks/urls.py
Users / Watchlist:
Watchlist list/create: included under /users/ (see core/core/urls.py) and implemented by users.views.WatchlistView
Consult the view implementations for request/response shapes:

core/stocks/views.py
core/users/views.py

Admin
Access Django admin at /admin/ after creating a superuser. Model admin customizations are in core/stocks/admin.py.

Notes & troubleshooting
The app will attempt to populate missing historical data via stocks.views.fetch_alpha_vantage_data. Ensure your Alpha Vantage API key is valid and you respect API rate limits.
If no local stocks exist for a sector/search, the code will try to create DB entries from Alpha Vantage or return helpful errors (see stocks.views.StockViewSet.search).

Contributing
Follow existing project structure under core/ apps.
Add tests in the tests.py files alongside apps and run python core/manage.py test.

Useful files
Project settings: core/core/settings.py
Stocks views & fetcher: core/stocks/views.py
Stocks routes: core/stocks/urls.py
Users views: core/users/views.py
Portfolios routes: core/portfolios/urls.py
Manage script: core/manage.py
Dependencies: requirements.txt