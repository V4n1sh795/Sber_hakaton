"""
Management команда для отправки напоминаний о событиях

Использование:
    python manage.py send_reminders
    
Можно добавить в cron для автоматического запуска:
    0 * * * * cd /path/to/project && python manage.py send_reminders
"""

from django.core.management.base import BaseCommand
from events.tasks import send_event_reminders


class Command(BaseCommand):
    help = 'Отправка напоминаний о предстоящих событиях (за 24 и 2 часа)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Начало проверки напоминаний...'))
        
        try:
            sent_count = send_event_reminders()
            
            if sent_count > 0:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Успешно отправлено {sent_count} напоминаний')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('⚠️ Напоминания для отправки не найдены')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Ошибка при отправке напоминаний: {e}')
            )
            raise
