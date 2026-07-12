from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404


def index(request):
    """Головна сторінка для Learning Log"""
    return render(request, "learning_logs/index.html")


# --- РОЗДІЛ: ТЕМИ (TOPICS) ---

@login_required
def topics(request):
    """Відображає ПРИВАТНІ теми поточного користувача."""
    # Шукаємо тільки ті, де is_public=False (приватні) і власник - це ти
    topics = Topic.objects.filter(owner=request.user, is_public=False).order_by("-date_added")
    context = {"topics": topics, "page_title": "Private Topics"}
    return render(request, "learning_logs/topics.html", context)


@login_required
def public_topics(request):
    """Відображає ПУБЛІЧНІ теми всіх користувачів."""
    # Шукаємо тільки ті, де is_public=True
    topics = Topic.objects.filter(is_public=True).order_by("-date_added")
    context = {"topics": topics, "page_title": "Public Topics"}
    # Використовуємо той самий шаблон, просто передаємо інші дані
    return render(request, "learning_logs/topics.html", context)


@login_required
def topic(request, topic_id):
    """Відображає окрему тему (і публічну, і приватну)."""
    topic = get_object_or_404(Topic, id=topic_id)

    # Якщо тема не публічна, перевіряємо, чи ти її власник
    if not topic.is_public:
        check_topic_owner(topic, request)

    entries = topic.entry_set.order_by("-date_added")
    context = {"topic": topic, "entries": entries}
    return render(request, "learning_logs/topic.html", context)


@login_required
def new_topic(request):
    """Додавання нової теми."""
    if request.method != "POST":
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            # Тут ми маємо отримувати галочку is_public з форми (додамо це в forms.py пізніше)
            new_topic.save()

            # Якщо тема публічна - кидаємо в публічний розділ, інакше в приватний
            if new_topic.is_public:
                return redirect("learning_logs:public_topics")
            return redirect("learning_logs:topics")

    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)


# --- РОЗДІЛ: ДОПИСИ (ENTRIES) ---

@login_required
def new_entry(request, topic_id):
    """Додавання нового допису."""
    topic = get_object_or_404(Topic, id=topic_id)

    if not topic.is_public:
        check_topic_owner(topic, request)

    if request.method != "POST":
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            # НОВЕ: Прив'язуємо допис до автора!
            new_entry.author = request.user
            new_entry.save()
            return redirect("learning_logs:topic", topic_id=topic_id)

    context = {"topic": topic, "form": form}
    return render(request, "learning_logs/new_entry.html", context)


@login_required
def edit_entry(request, entry_id):
    """Редагування допису."""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic

    # Забороняємо редагувати чужі дописи
    if entry.author != request.user:
        raise Http404

    if request.method != "POST":
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topic", topic_id=topic.id)

    context = {"entry": entry, "topic": topic, "form": form}
    return render(request, "learning_logs/edit_entry.html", context)


# --- РОЗДІЛ: ВИДАЛЕННЯ (DELETION) ---

@login_required
def delete_topic(request, topic_id):
    """Видаляє цілу тему та всі її дописи."""
    topic = get_object_or_404(Topic, id=topic_id)

    # Тільки власник може видалити тему
    check_topic_owner(topic, request)

    # Видаляємо (Django каскадно видалить всі дописи в ній)
    topic.delete()
    return redirect("learning_logs:topics")


@login_required
def delete_entry(request, entry_id):
    """Видаляє лише конкретний допис."""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic

    # Видалити допис може тільки його автор
    if entry.author != request.user:
        raise Http404

    entry.delete()
    return redirect("learning_logs:topic", topic_id=topic.id)


def check_topic_owner(topic, request):
    """Допоміжна функція: перевіряє, чи є юзер власником."""
    if topic.owner != request.user:
        raise Http404