from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Timetable, Teacher, Group, Subject, TimeSlot
from .forms import TimetableForm
from django.contrib.auth import logout


def home(request):
    return render(request, 'timetable/home.html')


class TimetableListView(ListView):
    model = Timetable
    template_name = 'timetable/timetable_list.html'
    context_object_name = 'timetable'

    def get_queryset(self):
        if not self.request.GET:
            return Timetable.objects.none()

        queryset = Timetable.objects.all()

        # Фільтрація за групою
        group = self.request.GET.get('group')
        if group:
            queryset = queryset.filter(group__name=group)

        # Фільтрація за викладачем
        teacher = self.request.GET.get('teacher')
        if teacher:
            queryset = queryset.filter(teacher__full_name=teacher)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Додаємо списки для фільтрів
        context['teachers'] = Teacher.objects.all()
        context['groups'] = Group.objects.all()
        # Збереження вибраних фільтрів
        context['selected_teacher'] = self.request.GET.get('teacher', '')
        context['selected_group'] = self.request.GET.get('group', '')

        context['search_performed'] = bool(self.request.GET)

        return context


# Міксин для перевірки, чи користувач є суперюзером або персоналом
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)

    def handle_no_permission(self):
        messages.error(self.request,
                       "У вас немає прав доступу для виконання цієї дії. Будь ласка, увійдіть як адміністратор.")
        return redirect('timetable:timetable_list')


# Захищені класи для створення, оновлення та видалення
class TimetableCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Timetable
    form_class = TimetableForm
    template_name = 'timetable/timetable_form.html'
    success_url = reverse_lazy('timetable:timetable_list')
    login_url = '/admin/login/'

    def form_valid(self, form):
        messages.success(self.request, "Новий запис успішно додано до розкладу!")
        return super().form_valid(form)


class TimetableUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Timetable
    form_class = TimetableForm
    template_name = 'timetable/timetable_form.html'
    success_url = reverse_lazy('timetable:timetable_list')
    login_url = '/admin/login/'

    def form_valid(self, form):
        messages.success(self.request, "Запис успішно оновлено!")
        return super().form_valid(form)


class TimetableDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Timetable
    template_name = 'timetable/timetable_confirm_delete.html'
    success_url = reverse_lazy('timetable:timetable_list')
    login_url = '/admin/login/'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Запис успішно видалено з розкладу!")
        return super().delete(request, *args, **kwargs)

def custom_logout(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.success(request, f"Ви успішно вийшли з системи, {username}!")
    return redirect('timetable:home')