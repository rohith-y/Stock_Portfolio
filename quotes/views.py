from django.shortcuts import render, redirect
from .models import Stock
from django.contrib import messages
from .forms import StockForm

 
def home(request):

	import requests
	import json

	if request.method == 'POST':
		ticker = request.POST['ticker']
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ticker+"/quote?token=pk_0f31a9253c034eb080303213d282996b")
		try:
			api= json.loads(api_request.content)

		except Exception as e:
			api = "Error...."

		return render(request, 'home.html', {'api':api}) 			
	else:
		return render(request, 'home.html', {'ticker': "Enter the required stock ticker you want to explore on"})

	

def about(request):
	return render(request, 'about.html', {})

def add_stock(request):

	import requests
	import json

	if request.method == 'POST':
		form = StockForm(request.POST or None)	

		if form.is_valid():
			form.save()
			messages.success(request,("Success the stock has been added"))
			return redirect('add_stock')
	else:
		ticker = Stock.objects.all()
		output = []
		for ticker_item in ticker:
				api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+str(ticker_item)+"/quote?token=pk_0f31a9253c034eb080303213d282996b")
				try:
					api= json.loads(api_request.content) 
					output.append(api)
				except Exception as e:
					api = "Error...."
		return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})

# pk_0f31a9253c034eb080303213d282996b

def delete(request, stock_id):
	item =Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock has been deleted Successfully"))
	return redirect(delete_stock)


def delete_stock(request):	
	ticker = Stock.objects.all()
	return render(request, 'delete_stock.html', {'ticker': ticker})

