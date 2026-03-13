from django import forms
from .models import Team, TeamMember, Repository, Department


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'department', 'manager', 'description', 'mission',
                  'responsibilities', 'slack_channel', 'email', 'status', 'upstream_dependencies']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'manager': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'mission': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'responsibilities': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'slack_channel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '#team-channel'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'upstream_dependencies': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '6'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude current team from dependencies if editing
        if self.instance.pk:
            self.fields['upstream_dependencies'].queryset = Team.objects.exclude(pk=self.instance.pk)


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['user', 'role', 'joined_at']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'joined_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class RepositoryForm(forms.ModelForm):
    class Meta:
        model = Repository
        fields = ['name', 'url', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
