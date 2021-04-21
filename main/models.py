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


class Item(models.Model):
    """Элемент."""

    # Идентификатор.
    id = models.SmallAutoField(primary_key=True, verbose_name='ИД')
    # Категория.
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='category',
        verbose_name='Категория'
    )
    # Заголовок.
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    # Текст.
    text = models.TextField(verbose_name='Текст')

    # Для отображения имени в списке редактирования Элемента в
    # место Item object(1).
    def __str__(self):
        return f'{self.title}'

    def to_dict(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'title': self.title,
            'text': self.text
        }

    class Meta:
        verbose_name = 'Элемент'
        verbose_name_plural = 'Элементы'
