# forms.py
from django import forms
from .models import *

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'


class TeamForm(forms.ModelForm):
    class meta:
        model = Stud_item
        fields = '__all__'

class Assign_StudentForm(forms.ModelForm):
    class Meta:
        model = Stud_item
        fields = ['stud', 'item', 'player_status', 'uty_team_selection', 'position', 'year']

    stud = forms.ModelChoiceField(queryset=Student.objects.all())
    item = forms.ModelChoiceField(queryset=Item.objects.all())

class SearchForm(forms.Form):
    uty_reg_no = forms.CharField(label='Enter Registration Number', max_length=50)

class AssignStudentForm(forms.ModelForm):
    class Meta:
        model = Stud_item
        fields = ['stud', 'item', 'player_status', 'uty_team_selection', 'position', 'year']

class StudItemForm(forms.ModelForm):
    class Meta:
        model = Stud_item
        fields = ['stud', 'item', 'player_status', 'uty_team_selection', 'position', 'year']


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'item', 'hour_1', 'hour_2', 'hour_3', 'hour_4', 'hour_5']


# class DepartmentForm(forms.ModelForm):
#     class Meta:
#         model = Department
#         fields = '__all__'

# class Sportform(forms.ModelForm):
#     class Meta:
#         model = Sport
#         fields = '__all__'


# class PlayerForm(forms.ModelForm):
#     class Meta:
#         fields = ['dob']
#         widgets = {
#             'dob': forms.DateInput(attrs={'type': 'date'}),
#         }
#         model = Player
#         fields = '__all__'  # Use all fields from the Player model