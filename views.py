import requests
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Stock
from .serializers import StockSerializer

# Function to get the real-time stock price from an API
def get_stock_price(ticker):
    api_key = 'YOUR_ALPHA_VANTAGE_API_KEY'  # Replace with your Alpha Vantage API key
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=5min&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    try:
        latest_time = next(iter(data['Time Series (5min)']))
        return float(data['Time Series (5min)'][latest_time]['4. close'])
    except KeyError:
        return None

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    @action(detail=False, methods=['get'])
    def total_value(self, request):
        stocks = Stock.objects.all()
        total_value = sum(stock.quantity * stock.current_price for stock in stocks)
        return Response({'total_value': total_value})

    def perform_create(self, serializer):
        stock = serializer.save()
        stock.current_price = get_stock_price(stock.ticker)
        stock.save()


# Create your views here.
