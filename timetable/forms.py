from django import forms
from .models import Timetable, Teacher, Subject, Group, TimeSlot


class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['day_of_week', 'time_slot', 'subject', 'teacher', 'group', 'room']
        widgets = {
            'day_of_week': forms.Select(attrs={'class': 'form-select'}),
            'time_slot': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'teacher': forms.Select(attrs={'class': 'form-select'}),
            'group': forms.Select(attrs={'class': 'form-select'}),
            'room': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер аудиторії'
            }),
        }
        labels = {
            'day_of_week': 'День тижня',
            'time_slot': 'Час проведення',
            'subject': 'Предмет',
            'teacher': 'Викладач',
            'group': 'Група',
            'room': 'Аудиторія',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Встановленнях всіх полів як обов'язкових
        for field_name, field in self.fields.items():
            field.required = True

        # Налаштування queryset для випадаючих списків
        if TimeSlot.objects.exists():
            self.fields['time_slot'].queryset = TimeSlot.objects.all()
        else:
            self.fields['time_slot'].empty_label = "Спочатку додайте часові проміжки в адмін-панелі"

        if Subject.objects.exists():
            self.fields['subject'].queryset = Subject.objects.all()
        else:
            self.fields['subject'].empty_label = "Спочатку додайте предмети в адмін-панелі"

        if Teacher.objects.exists():
            self.fields['teacher'].queryset = Teacher.objects.all()
        else:
            self.fields['teacher'].empty_label = "Спочатку додайте викладачів в адмін-панелі"

        if Group.objects.exists():
            self.fields['group'].queryset = Group.objects.all()
        else:
            self.fields['group'].empty_label = "Спочатку додайте групи в адмін-панелі"

    def clean_room(self):
        """Валідація аудиторії"""
        room = self.cleaned_data.get('room')
        if room:
            room = room.strip()
            if not room:
                raise forms.ValidationError("Поле аудиторії не може бути порожнім")
            if len(room) > 50:
                raise forms.ValidationError("Назва аудиторії занадто довга (максимум 50 символів)")
        return room