from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import os
import requests
import random
import json
from nearBackExercise.settings import SEC_KEY

def index(request):
    current_location = os.getcwd()

    # Use default data to get a full list (found in https://www.sec.gov/file/company-tickers)
    default_data = {}
    with open(current_location + '/publicCompanies/assets/companies.json') as f:
        default_data = json.load(f)

    # Get a random company
    random_company = random.randint(0, len(default_data))
    company = default_data[str(random_company)]
    company_ticker = company['ticker']

    # Fetch data from SEC API
    data = requests.get(f'https://api.sec-api.io/mapping/ticker/{company_ticker}?token={SEC_KEY}')
    data = json.loads(data.content)

    context = {
        'name': data[0]['name'],
        'ticker': data[0]['ticker'],
        'cik': data[0]['cik'],
        'exchange': data[0]['exchange']
    }
    print('==================================')
    print('name: ' + context['name'])
    print('ticker: ' + context['ticker'])
    print('cik: ' + context['cik'])
    print('exchange: ' + context['exchange'])
    print('==================================')

    return render(request, "publicCompanies/index.html", context)
