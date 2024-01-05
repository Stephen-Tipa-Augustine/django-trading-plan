from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets

from . import serializers
from . import models


# Create your views here.
@login_required(login_url='plan:login')
def index(request):
    return_list = []
    info = models.Info.objects.filter(user=request.user)
    returns = models.ActualReturns.objects.filter(user=request.user)
    for i in returns:
        return_list.append({
            'id': i.id,
            'user': i.user.id,
            'value': i.value,
            'day': i.day
        })
    trade_data = []
    if len(info) != 0:
        user_info = info[0]
        over_under_total = 0
        for i in range(1, 32):
            data = {'day': i}
            if i == 1:
                data['starting_balance'] = round(user_info.starting_balance, 3)
            else:
                data['starting_balance'] = round(trade_data[i - 2]['starting_balance'] + trade_data[i - 2]['target'], 3)

            data['target'] = round(data['starting_balance'] * user_info.growth / 100, 3)
            for j in returns:
                if i == j.day:
                    data['actual'] = round(j.value, 3)
                    break
            else:
                data['actual'] = 0
            if data['actual'] == 0:
                data['over_under'] = 0
            else:
                data['over_under'] = round(data['actual'] - data['target'], 3)
            over_under_total += data['over_under']
            data['over_under_total'] = round(over_under_total, 3)

            trade_data.append(data)
    return render(request, 'index.html',
                  context={'user': {'id': request.user.id, 'username': request.user.username},
                           'data': trade_data})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('plan:homepage')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'auth_form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return render(request, 'logout.html')


# Create your views here.
class InfoFormViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = models.Info.objects.all()
    serializer_class = serializers.InfoFormSerializer


class ActualReturnsViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = models.ActualReturns.objects.all()
    serializer_class = serializers.ActualReturnsFormSerializer
