from django.shortcuts import render, redirect
import yfinance as yf
import os
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def fetch_data():
    ticker = os.getenv('TICKER', '^GSPC')
    days = os.getenv('DAYS', '7')
    interval = os.getenv('INTERVAL', '1h')
    data = yf.download(tickers=ticker, period=f'{days}d', interval=interval)
    data = data.drop(columns=['Volume'])  # Drop the 'Volume' column
    data['Date'] = data.index  # Add 'Date' column from index
    data['Date'] = data['Date'].apply(lambda x: x.isoformat())  # Convert all Timestamps to strings
    return data.reset_index(drop=True).to_dict('records')  # Drop the original index


def candlestick_view(request):
    if 'data' not in request.session:
        request.session['data'] = fetch_data()
        request.session['index'] = random.randint(0, len(request.session['data']) - 1)
    
    index = request.session['index']
    candlestick = request.session['data'][index]

    # Debug prints
    print(f"Date: {candlestick['Date']}, Type: {type(candlestick['Date'])}")
    print(f"Close: {candlestick['Close']}, Type: {type(candlestick['Close'])}")
    print(f"High: {candlestick['High']}, Type: {type(candlestick['High'])}")
    print(f"Low: {candlestick['Low']}, Type: {type(candlestick['Low'])}")
    print(f"Open: {candlestick['Open']}, Type: {type(candlestick['Open'])}")

    is_last = index == len(request.session['data']) - 1
    # candlestick['Date'] = candlestick['Date'].isoformat()
    # print(f"After isoformat: {candlestick['Date']}, Type: {type(candlestick['Date'])}")
    return render(request, 'labeller/candlestick.html', {
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


@csrf_exempt
def check_doji(request):
    if request.method == 'POST':
        index = request.session['index']
        candlestick = request.session['data'][index]
        user_choice = request.POST.get('choice')
        is_doji = abs(candlestick['Open'] - candlestick['Close']) < 0.001  # Adjust this condition as needed
        is_correct = (user_choice == 'doji' and is_doji) or (user_choice == 'not_doji' and not is_doji)
        if is_correct:
            request.user.token += 1
            request.user.save()
        return JsonResponse({'is_correct': is_correct, 'token': request.user.token})