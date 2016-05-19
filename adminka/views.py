#from django_admin import settings
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.conf import settings
from . import models
from . import forms
from models import Player, PlayerAchievement, PlayerSession, Achievement
from django.db.models import F, Count



@login_required
def player_home(request):
    return render(request, 'player_home.html')


@login_required
def player_all(request):
    form = forms.PlayerForm()
    message = ''
    if 'email' in request.GET:
        player_list = Player.objects.filter(email__icontains=request.GET['email']).annotate(count=Count('playerachievement'))
        if len(player_list) == 0:
           message = 'WRONG EMAIL!'
    else:
        player_list = Player.objects.all().annotate(count=Count('playerachievement'))

    paginator = Paginator(player_list, settings.PAGINATOR_VALUE)
    page = request.GET.get('page')
    try:
        player_list = paginator.page(page)
    except PageNotAnInteger:
        player_list = paginator.page(1)
    except EmptyPage:
        player_list = paginator.page(paginator.num_pages)
    template_data = {
        "form": form,
        "message": message,
        "player": player_list,
    }
    return render(request, 'player_all.html', template_data)


@login_required
def change_xp(request, player_id):
    message_value_add = ''
    message_value_remove = ''
    player = models.Player.objects.get(id=player_id)
    form = forms.PlayerXpForm()
    player_xp = player.xp
    if request.method == 'POST' and 'xp_add' in request.POST:
        form = forms.PlayerXpForm(request.POST)
        if form.is_valid():
            player_xp = player.xp + form.cleaned_data['xp']
            player.xp = F('xp') + form.cleaned_data['xp']
            if player_xp <= 2147483647:
                player.save()
            else:
                message_value_add = "Player's xp is more than 2147483647, cant save value"
    if request.method == 'POST' and 'xp_remove' in request.POST:
        form = forms.PlayerXpForm(request.POST)
        if form.is_valid():
            if player.xp >= form.cleaned_data['xp']:
                player_xp = player.xp - form.cleaned_data['xp']
                player.xp = F('xp') - form.cleaned_data['xp']
                player.save()

            else:
                message_value_remove = "Player's xp is less than 0, cant save value"
    template_data = {
        "form_add": form,
        "message_value_add": message_value_add,
        "message_value_remove": message_value_remove,
        "player": player,
        "player_xp": player_xp,
    }
    return render(request, 'player_xp.html', template_data)


@login_required
def player_filter(request):
    player_list = []
    kwargs = {}
    form_filter_xp = forms.PlayerFilterXp()
    form_filter_session = forms.PlayerFilterSession()

    if request.method == 'POST' and 'filter_session' in request.POST:
        form_filter_session = forms.PlayerFilterSession(request.POST)
        if form_filter_session.is_valid():
            if form_filter_session.cleaned_data['choises'] == "gte":
                kwargs = {'count_session__gte': form_filter_session.cleaned_data['count_session']}
            elif form_filter_session.cleaned_data['choises'] == "lte":
                kwargs = {'count_session__lte': form_filter_session.cleaned_data['count_session']}
            player_list = Player.objects.annotate(count_session=Count('sessions')).filter(**kwargs)

    if request.method == 'POST' and 'filter_xp' in request.POST:
        form_filter_xp = forms.PlayerFilterXp(request.POST)
        if form_filter_xp.is_valid():
            if form_filter_xp.cleaned_data['choises'] == "gte":
                kwargs = {'xp__gte': form_filter_xp.cleaned_data['count_xp']}
            elif form_filter_xp.cleaned_data['choises'] == "lte":
                kwargs = {'xp__lte': form_filter_xp.cleaned_data['count_xp']}
            player_list = Player.objects.filter(**kwargs)

    paginator = Paginator(player_list, settings.PAGINATOR_VALUE)
    page = request.GET.get('page')
    try:
        player_list = paginator.page(page)
    except PageNotAnInteger:
        player_list = paginator.page(1)
    except EmptyPage:
        player_list = paginator.page(paginator.num_pages)

    template_data = {
        "form_filter_session": form_filter_session,
        "form_filter_xp": form_filter_xp,
        "player": player_list,
    }
    return render(request, 'player_filter.html', template_data)

@login_required
def player_achievement(request, player_id):
    temp = None
    player_achievement = models.PlayerAchievement()
    player = models.Player.objects.get(id=player_id)
    player_xp = player.xp
    form_achievement = forms.PlayerAchievement()
    achievement_list = PlayerAchievement.objects.filter(player=player.id).values('achievement__name').annotate(count=Count('achievement__name'))
    if request.method == 'POST':
        form_achievement = forms.PlayerAchievement(request.POST)
        if form_achievement.is_valid():
            temp = Achievement.objects.filter(name=form_achievement.cleaned_data['achievement'])
            player_xp = player.xp + temp[0].xp
            player.xp = F('xp') + temp[0].xp
            player.save()
            player_achievement = models.PlayerAchievement(player=player, achievement=temp[0])
            player_achievement.save()

    template_data = {
        "form_achievement": form_achievement,
        "achievement": achievement_list,
        "player": player,
        "player_xp": player_xp,
    }
    return render(request, 'player_achievement.html', template_data)

@login_required
def player_achievement_list(request, player_id):
    player = models.Player.objects.get(id=player_id)
    achievement_list = PlayerAchievement.objects.filter(player=player.id).values('achievement__name', 'achievement__xp', 'created')

    template_data = {
        "achievement": achievement_list,
        "player": player,
    }
    return render(request, 'player_achievement_list.html', template_data)





