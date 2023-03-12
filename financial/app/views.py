from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import FinancialDataModel
from .serializers import FinancialDataModelSerializer
import json
from django.shortcuts import HttpResponse
from django.db.models import Avg, Sum
from django.http import JsonResponse
import datetime

# Create your views here.
def get_financial_data(request):

    # Get parameters from request
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    symbol = request.GET.get('symbol', None)
    limit = request.GET.get('limit', 5)
    page = request.GET.get('page', 1)

    # Instead of just giving a error message, we specify error information
    errors = {}
    if start_date is not None and end_date is not None and start_date > end_date:
        errors['date'] = 'start_date should be less than or equal to end_date'
    if limit is not None:
        try:
            limit = int(limit)
        except ValueError:
            errors['limit'] = 'limit should be an integer'
    if page is not None:
        try:
            page = int(page)
        except ValueError:
            errors['page'] = 'page should be an integer'
    if errors:
        response_data = {'info': errors}
        return JsonResponse(response_data, status=400)

    # Build query
    query = FinancialDataModel.objects.all()
    query = query.order_by('date')

    if start_date is not None:
        query = query.filter(date__gte=start_date)
    if end_date is not None:
        query = query.filter(date__lte=end_date)
    if symbol is not None:
        query = query.filter(symbol=symbol)

    # Paginate results
    paginator = Paginator(query, limit)
    try:
        page_data = paginator.page(page)
    except ValidationError:
        response_data = {'info': 'Invalid page number'}
        return JsonResponse(response_data, status=400)

    # Build response data
    data = []
    for obj in page_data:
        obj_data = {
            'symbol': obj.symbol,
            'date': obj.date.strftime('%Y-%m-%d'),
            'open_price': obj.open_price,
            'close_price': obj.close_price,
            'volume': obj.volume,
        }
        data.append(obj_data)

    # Build response object
    result = {'data': data}

    # Add pagination info
    result['pagination'] = {
        'count': paginator.count,
        'page': page_data.number,
        'limit': page_data.paginator.per_page,
        'pages': paginator.num_pages,
    }
    
    # Add info
    result['info'] = {'error': ''}

    return JsonResponse(result, safe=False)

def get_statistics(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    symbol = request.GET.get('symbol')
    
    try:
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        return JsonResponse({'info': 'Invalid date format. Please use yyyy-mm-dd.'}, status=400)

    if symbol is None:
        return JsonResponse({'info': 'Symbol is required.'}, status=400)
    
    data = {}
    try:
        financial_data = FinancialDataModel.objects.filter(symbol=symbol, date__gte=start_date, date__lte=end_date)

        data['average_daily_open_price'] = financial_data.aggregate(Avg('open_price'))['open_price__avg']
        data['average_daily_closing_price'] = financial_data.aggregate(Avg('close_price'))['close_price__avg']
        data['average_daily_volume'] = financial_data.aggregate(Avg('volume'))['volume__avg']
        
        return JsonResponse({'data': data, 'info': {'error': ''}}, status=200)
    except FinancialDataModel.DoesNotExist:
        return JsonResponse({'info': {'error': 'No financial data found for the given symbol and date range.'}}, status=404)
    except Exception as e:
        return JsonResponse({'info': {'error': str(e)}}, status=500)