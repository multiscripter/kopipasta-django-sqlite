from django.db import models


class Category(models.Model):
    """Категория."""

    # Идентификатор.
    id = models.SmallAutoField(primary_key=True, verbose_name='ИД')
    # Название.
    name = models.CharField(max_length=128, verbose_name='Название')

    # Для отображения имени в списке редактирования Элемента
    # вместо Category object(1).
    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
