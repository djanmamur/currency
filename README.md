# Currency API

Simple application to retrieve and/or scrape
currency data from Uzbekistan banks

Currently, 4 financial institutions are supported:
```
Central Bank
National Bank of Uzbekistan
Orient Finance Bank
Kapital Bank 
```

`GET` `/currency`

```json
Content-Type application/json
200 OK

[
  {
    "bank_name": "CENTRAL_BANK",
    "currency_data": [
      {
        "buy": "10139.30",
        "currency": "USD",
        "sell": "-"
      },
      {
        "buy": "11051.84",
        "currency": "EUR",
        "sell": "-"
      },
      {
        "buy": "141.35",
        "currency": "RUB",
        "sell": "-"
      },
      {
        "buy": "12333.44",
        "currency": "GBP",
        "sell": "-"
      }
    ]
  },
  {
    "bank_name": "OFB",
    "currency_data": [
      {
        "buy": "10100.00",
        "currency": "USD",
        "sell": "10200.00"
      },
      {
        "buy": "10500.00",
        "currency": "EUR",
        "sell": "12000.00"
      },
      {
        "buy": "11000.00",
        "currency": "GBP",
        "sell": "13000.00"
      },
      {
        "buy": "9500.00",
        "currency": "CHF",
        "sell": "11000.00"
      },
      {
        "buy": "90.00",
        "currency": "JPY",
        "sell": "100.00"
      }
    ]
  },
  {
    "bank_name": "NBU",
    "currency_data": [
      {
        "buy": "10600.00",
        "currency": "EUR",
        "sell": "11200.00"
      },
      {
        "buy": "11500.00",
        "currency": "GBP",
        "sell": "12400.00"
      },
      {
        "buy": "110.00",
        "currency": "RUB",
        "sell": "145.00"
      },
      {
        "buy": "10100.00",
        "currency": "USD",
        "sell": "10160.00"
      }
    ]
  },
  {
    "bank_name": "KAPITAL_BANK",
    "currency_data": [
      {
        "buy": "10490",
        "currency": "EUR",
        "sell": "11650"
      },
      {
        "buy": "10120",
        "currency": "USD",
        "sell": "10170"
      },
      {
        "buy": "11960",
        "currency": "GBP",
        "sell": "12760"
      },
      {
        "buy": "141",
        "currency": "RUB",
        "sell": "145"
      }
    ]
  }
]
```
    