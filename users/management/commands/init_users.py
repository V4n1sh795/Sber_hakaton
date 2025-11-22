"""
Management команда для инициализации системы пользователей

Создает:
1. Суперадмина (superuser) - полный доступ к системе
2. Staff-пользователя (библиотекарь) - для управления обычными пользователями

Использование:
    python manage.py init_users
"""
from django.core.management.base import BaseCommand
from users.models import CustomUser
from django.db import transaction


class Command(BaseCommand):
    help = 'Инициализация пользователей системы (superadmin и staff)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--superadmin-email',
            type=str,
            default='admin@library.local',
            help='Email суперадмина'
        )
        parser.add_argument(
            '--superadmin-password',
            type=str,
            default='admin123',
            help='Пароль суперадмина'
        )
        parser.add_argument(
            '--staff-email',
            type=str,
            default='librarian@library.local',
            help='Email сотрудника библиотеки'
        )
        parser.add_argument(
            '--staff-password',
            type=str,
            default='librarian123',
            help='Пароль сотрудника библиотеки'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Пересоздать пользователей если они уже существуют'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        superadmin_email = options['superadmin_email']
        superadmin_password = options['superadmin_password']
        staff_email = options['staff_email']
        staff_password = options['staff_password']
        force = options['force']

        self.stdout.write(self.style.NOTICE('Инициализация пользователей...'))

        # Создание суперадмина
        if CustomUser.objects.filter(email=superadmin_email).exists():
            if force:
                CustomUser.objects.filter(email=superadmin_email).delete()
                self.stdout.write(self.style.WARNING(f'Удален существующий суперадмин: {superadmin_email}'))
            else:
                self.stdout.write(self.style.WARNING(f'Суперадмин уже существует: {superadmin_email}'))
        
        if not CustomUser.objects.filter(email=superadmin_email).exists():
            CustomUser.objects.create_superuser(
                username=superadmin_email,
                email=superadmin_email,
                password=superadmin_password,
                name='Администратор',
                lastname='Системы'
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Создан суперадмин: {superadmin_email}'))
            self.stdout.write(self.style.NOTICE(f'  Пароль: {superadmin_password}'))

        # Создание staff-пользователя (библиотекарь)
        if CustomUser.objects.filter(email=staff_email).exists():
            if force:
                CustomUser.objects.filter(email=staff_email).delete()
                self.stdout.write(self.style.WARNING(f'Удален существующий staff: {staff_email}'))
            else:
                self.stdout.write(self.style.WARNING(f'Staff пользователь уже существует: {staff_email}'))
        
        if not CustomUser.objects.filter(email=staff_email).exists():
            CustomUser.objects.create_user(
                username=staff_email,
                email=staff_email,
                password=staff_password,
                name='Библиотекарь',
                lastname='Общий',
                is_staff=True
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Создан сотрудник: {staff_email}'))
            self.stdout.write(self.style.NOTICE(f'  Пароль: {staff_password}'))

        self.stdout.write(self.style.SUCCESS('\n=== Инициализация завершена ==='))
        self.stdout.write(self.style.NOTICE('\nДоступ к админ-панели: /admin/'))
        self.stdout.write(self.style.NOTICE('Суперадмин имеет полный доступ'))
        self.stdout.write(self.style.NOTICE('Staff может управлять пользователями через API'))
