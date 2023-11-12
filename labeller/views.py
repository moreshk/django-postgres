from django.shortcuts import render, redirect
import yfinance as yf
import os
import random

def fetch_data():
    ticker = os.getenv('TICKER', '^GSPC')
    days = os.getenv('DAYS', '7')
    interval = os.getenv('INTERVAL', '1h')
    data = yf.download(tickers=ticker, period=f'{days}d', interval=interval)
    return data.reset_index().to_dict('records')

def candlestick_view(request):
    if 'data' not in request.session:
        request.session['data'] = fetch_data()
        request.session['index'] = random.randint(0, len(request.session['data']) - 1)
    
    index = request.session['index']
    candlestick = request.session['data'][index]
    return render(request, 'candlestick.html', {
        'candlestick': candlestick,
        'index': index,
        'total': len(request.session['data']),
    })

def back_view(request):
    if request.session['index'] > 0:
        request.session['index'] -= 1
    return redirect('candlestick_view')

def forward_view(request):
    if request.session['index'] < len(request.session['data']) - 1:
        request.session['index'] += 1
    return redirect('candlestick_view')