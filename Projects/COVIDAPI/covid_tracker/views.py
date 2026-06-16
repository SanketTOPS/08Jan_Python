import requests
from django.shortcuts import render

def covid_stats(request):
    url = "https://api.rootnet.in/covid19-in/stats/latest"
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get('success'):
            summary = data['data']['summary']
            regional = data['data']['regional']
            last_refreshed = data['lastRefreshed']
            
            context = {
                'summary': summary,
                'regional': regional,
                'last_refreshed': last_refreshed,
                'success': True
            }
        else:
            context = {'success': False, 'error': 'Failed to fetch data from API'}
            
    except Exception as e:
        context = {'success': False, 'error': str(e)}
        
    return render(request, 'covid_tracker/index.html', context)
