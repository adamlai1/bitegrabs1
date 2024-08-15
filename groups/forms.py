from django import forms
from .models import Group
from .models import GroupMember

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
class InviteMemberForm(forms.ModelForm):
    class Meta:
        model = GroupMember
        fields = ['user', 'location', 'preferences']
FOOD_CHOICES = [
    ('pizza', 'Pizza'),
    ('chinese', 'Chinese'),
    ('mexican', 'Mexican'),
    ('italian', 'Italian'),
    ('indian', 'Indian'),
    ('japanese', 'Japanese'),
    # Add more categories as needed
]

class GroupMemberForm(forms.ModelForm):
    preferences = forms.MultipleChoiceField(
        choices=FOOD_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Food Preferences"
    )

    class Meta:
        model = GroupMember
        fields = ['location', 'preferences']