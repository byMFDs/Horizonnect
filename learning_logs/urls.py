"""Defines URL patterns for learning_logs."""

from django.urls import path
from . import views

app_name = "learning_logs"

urlpatterns = [
    # Головна сторінка
    path("", views.index, name="index"),

    # Твій приватний сектор (тільки твої приватні теми)
    path("topics/", views.topics, name="topics"),

    # НОВЕ: Публічний сектор (теми, які бачать усі)
    path("topics/public/", views.public_topics, name="public_topics"),

    # Сторінка конкретної теми (і публічної, і приватної)
    path("topics/<int:topic_id>/", views.topic, name="topic"),

    # Додавання та редагування
    path("new_topic/", views.new_topic, name="new_topic"),
    path("new_entry/<int:topic_id>/", views.new_entry, name="new_entry"),
    path("edit_entry/<int:entry_id>/", views.edit_entry, name="edit_entry"),

    # НОВЕ: Видалення теми та допису
    path("delete_topic/<int:topic_id>/", views.delete_topic, name="delete_topic"),
    path("delete_entry/<int:entry_id>/", views.delete_entry, name="delete_entry"),
]