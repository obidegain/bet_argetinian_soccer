from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse
from .models import Bet


@login_required(login_url="/login/")
def bet_list(request):
    user_bets = Bet.objects.filter(user=request.user)
    context = {
        'user_bets': user_bets
    }
    return render(request, 'bet_list.html', context)


#@login_required
def bet_edit(request, pk):
    bet = get_object_or_404(Bet, pk=pk, user=request.user)
    if request.method == 'POST':
        bet.result_home = request.POST.get('result_home')
        bet.result_away = request.POST.get('result_away')
        bet.save()
    context = {
        'bet': bet
    }
    return render(request, 'bet_edit.html', context)



#@login_required
def bet_list_edit(request):
    bets = Bet.objects.filter(user=request.user)
    if request.method == 'POST':
        for bet in bets:
            bet.result_home = request.POST.get(f"result_home_{bet.pk}")
            bet.result_away = request.POST.get(f"result_away_{bet.pk}")
            bet.save()
        return redirect(reverse('bet_list'))
    context = {
        'bets': bets
    }
    return render(request, 'bet_list_edit.html', context)