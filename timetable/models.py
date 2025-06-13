from django.db import models

class Teacher(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="Повне ім'я викладача")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Викладач"
        verbose_name_plural = "Викладачі"
        ordering = ['full_name']


class Subject(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва предмету")
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Викладач")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предмети"
        ordering = ['name']


class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name="Назва групи")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Група"
        verbose_name_plural = "Групи"
        ordering = ['name']


class TimeSlot(models.Model):
    time_slot = models.CharField(max_length=50, unique=True, verbose_name="Часовий проміжок")

    def __str__(self):
        return self.time_slot

    class Meta:
        verbose_name = "Часовий проміжок"
        verbose_name_plural = "Часові проміжки"
        ordering = ['id']


class Timetable(models.Model):
    DAY_CHOICES = [
        ('Понеділок', 'Понеділок'),
        ('Вівторок', 'Вівторок'),
        ('Середа', 'Середа'),
        ('Четвер', 'Четвер'),
        ('П`ятниця', 'П`ятниця'),
        ('Субота', 'Субота'),
    ]

    day_of_week = models.CharField(max_length=255, choices=DAY_CHOICES, verbose_name="День")
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, verbose_name="Час проведення")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Викладач")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Група")
    room = models.CharField(max_length=255, verbose_name="Аудиторія")

    def __str__(self):
        return f"{self.day_of_week}, {self.time_slot}, {self.subject}"

    class Meta:
        verbose_name = "Розклад"
        verbose_name_plural = "Розклад"
        ordering = ['day_of_week', 'time_slot']