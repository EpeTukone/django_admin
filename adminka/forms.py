from django import forms
import models


CHOICES = (
        ('gte', '>='),
        ('lte', '<='),
    )


class PlayerForm(forms.Form):
    email = forms.CharField(label='Email', max_length=45)


class PlayerXpForm(forms.Form):
    xp = forms.IntegerField(label='Xp', min_value=0, max_value=2147483647)


class PlayerFilterSession(forms.Form):
    choises = forms.ChoiceField(label='Sessions count', choices=CHOICES, required=True)
    count_session = forms.IntegerField(min_value=0, label='')


class PlayerFilterXp(forms.Form):
    choises = forms.ChoiceField(label='Xp count', choices=CHOICES, required=True)
    count_xp = forms.IntegerField(min_value=0, label='')


class PlayerAchievement(forms.Form):

    achievement = forms.ModelChoiceField(label='Select achievement from list', required=False, queryset=models.Achievement.objects.all())

