"""
Задачи для отправки напоминаний о событиях

Этот модуль содержит функции для отправки напоминаний пользователям
о предстоящих событиях. Поддерживается как Django management command,
так и интеграция с Celery для автоматической отправки.
"""

from celery import shared_task

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
import logging

from .models import EventSubscription

logger = logging.getLogger(__name__)
User = get_user_model()


def send_event_reminders():
    """
    Отправка напоминаний о предстоящих событиях (основная функция)
    
    Проверяет активные подписки и отправляет email напоминания:
    - За 24 часа до начала события
    - За 2 часа до начала события
    
    Использование:
    - Как management command: python manage.py send_reminders
    - Как Celery task: запускать периодически (например, каждый час)
    - Вручную через Django shell
    
    Returns:
        int: Количество отправленных напоминаний
    """
    now = timezone.now()
    
    # Временные окна для напоминаний (с погрешностью ±10 минут)
    window_24h_start = now + timedelta(hours=23, minutes=50)
    window_24h_end = now + timedelta(hours=24, minutes=10)
    
    window_2h_start = now + timedelta(hours=1, minutes=50)
    window_2h_end = now + timedelta(hours=2, minutes=10)
    
    sent_count = 0
    
    # Обработка напоминаний за 24 часа
    subscriptions_24h = EventSubscription.objects.filter(
        status='active',
        reminder_type__in=['24h', 'both'],
        reminder_24h_sent=False,
        event__start_date__range=(window_24h_start, window_24h_end)
    ).select_related('event', 'user')
    
    logger.info(f"Найдено {subscriptions_24h.count()} подписок для напоминаний за 24 часа")
    
    for subscription in subscriptions_24h:
        try:
            send_reminder_email(
                subscription=subscription,
                hours_before=24
            )
            subscription.reminder_24h_sent = True
            subscription.save(update_fields=['reminder_24h_sent'])
            sent_count += 1
            logger.info(f"✅ Напоминание 24h отправлено: {subscription.user.email}")
        except Exception as e:
            logger.error(f"❌ Ошибка отправки напоминания 24h для {subscription.user.email}: {e}")
    
    # Обработка напоминаний за 2 часа
    subscriptions_2h = EventSubscription.objects.filter(
        status='active',
        reminder_type__in=['2h', 'both'],
        reminder_1h_sent=False,  # используем поле reminder_1h_sent для 2h
        event__start_date__range=(window_2h_start, window_2h_end)
    ).select_related('event', 'user')
    
    logger.info(f"Найдено {subscriptions_2h.count()} подписок для напоминаний за 2 часа")
    
    for subscription in subscriptions_2h:
        try:
            send_reminder_email(
                subscription=subscription,
                hours_before=2
            )
            subscription.reminder_1h_sent = True
            subscription.save(update_fields=['reminder_1h_sent'])
            sent_count += 1
            logger.info(f"✅ Напоминание 2h отправлено: {subscription.user.email}")
        except Exception as e:
            logger.error(f"❌ Ошибка отправки напоминания 2h для {subscription.user.email}: {e}")
    
    logger.info(f"📧 Всего отправлено напоминаний: {sent_count}")
    return sent_count


def send_reminder_email(subscription, hours_before):
    """
    Отправка email напоминания о событии
    
    Args:
        subscription: объект EventSubscription
        hours_before: количество часов до события (24 или 2)
    """
    event = subscription.event
    user = subscription.user
    
    subject = f'📚 Напоминание: {event.name}'
    
    hours_text = "24 часа" if hours_before == 24 else "2 часа"
    
    message = f"""Здравствуйте, {user.full_name}!

Напоминаем, что через {hours_text} начнётся событие, на которое вы подписаны:

📅 Событие: {event.name}
🕐 Начало: {event.start_date.strftime('%d.%m.%Y в %H:%M')}
🕑 Окончание: {event.end_date.strftime('%d.%m.%Y в %H:%M')}

{event.description if event.description else ''}

До встречи на событии!

---
Это автоматическое уведомление. Если вы хотите отписаться от напоминаний,
войдите в свой профиль на сайте библиотеки."""
    
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@library.ru')
    recipient_list = [user.email]
    
    try:
        logger.info(f"📧 Отправка письма для {user.email}...")
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        logger.info(f"✅ Письмо успешно отправлено: {user.email}")
    except Exception as e:
        logger.error(f"❌ Ошибка отправки письма {user.email}: {e}")
        raise

@shared_task
def send_event_reminders_task():
    """
    Celery задача для периодической отправки напоминаний
    
    Returns:
        int: Количество отправленных напоминаний
    """
    logger.info("🔔 Запуск Celery задачи: проверка напоминаний о событиях")
    return send_event_reminders()


@shared_task
def send_subscription_confirmation_email(subscription_id):
    """
    Отправка подтверждения подписки на событие (опционально)
    
    Args:
        subscription_id: ID подписки EventSubscription
    """
    try:
        subscription = EventSubscription.objects.select_related('event', 'user').get(id=subscription_id)
        event = subscription.event
        user = subscription.user
        
        subject = f'✅ Подписка на событие: {event.name}'
        
        reminder_text = {
            'none': 'без напоминаний',
            '24h': 'за 24 часа до события',
            '2h': 'за 2 часа до события',
            'both': 'за 24 и 2 часа до события',
        }.get(subscription.reminder_type, 'без напоминаний')
        
        message = f"""
Здравствуйте, {user.full_name}!

Вы успешно подписались на событие:

📅 Событие: {event.name}
🕐 Начало: {event.start_date.strftime('%d.%m.%Y в %H:%M')}
🕑 Окончание: {event.end_date.strftime('%d.%m.%Y в %H:%M')}

Тип напоминаний: {reminder_text}

{event.description if event.description else ''}

До встречи на событии!
        """.strip()
        
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@library.ru')
        
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        logger.info(f"✅ Подтверждение подписки отправлено: {user.email}")
        return f"Confirmation sent to {user.email}"
        
    except EventSubscription.DoesNotExist:
        logger.error(f"❌ Подписка {subscription_id} не найдена")
        return f"Subscription {subscription_id} not found"
    except Exception as e:
        logger.error(f"❌ Ошибка отправки подтверждения: {str(e)}")
        return f"Error: {str(e)}"
