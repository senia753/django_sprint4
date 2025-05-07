from django.shortcuts import render


def about(request):
    return render(request, 'pages/about.html')


def rules(request):
    return render(request, 'pages/rules.html')

def handler403(request, exception):
    return render(request, 'pages/403csrf.html', status=403)

def handler404(request, exception):
    return render(request, 'pages/404.html', status=404)

def handler500(request):
    return render(request, 'pages/500.html', status=500)
