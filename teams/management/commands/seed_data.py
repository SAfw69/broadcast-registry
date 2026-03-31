"""
Management command to populate the database with sample data.
Run with: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from teams.models import Department, Team, TeamMember, Repository
from django.utils import timezone
import datetime

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with sample Broadcast Company engineering team data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Create superuser/admin
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@broadcast.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS('Created admin user (admin/admin123)'))
        else:
            admin = User.objects.get(username='admin')

        # Create regular users (engineers)
        engineers_data = [
            ('alice.johnson', 'Alice', 'Johnson', 'alice@broadcast.com'),
            ('bob.smith', 'Bob', 'Smith', 'bob@broadcast.com'),
            ('carol.white', 'Carol', 'White', 'carol@broadcast.com'),
            ('david.brown', 'David', 'Brown', 'david@broadcast.com'),
            ('emma.davis', 'Emma', 'Davis', 'emma@broadcast.com'),
            ('frank.miller', 'Frank', 'Miller', 'frank@broadcast.com'),
            ('grace.wilson', 'Grace', 'Wilson', 'grace@broadcast.com'),
            ('henry.moore', 'Henry', 'Moore', 'henry@broadcast.com'),
            ('iris.taylor', 'Iris', 'Taylor', 'iris@broadcast.com'),
            ('james.anderson', 'James', 'Anderson', 'james@broadcast.com'),
            ('kate.thomas', 'Kate', 'Thomas', 'kate@broadcast.com'),
            ('liam.jackson', 'Liam', 'Jackson', 'liam@broadcast.com'),
            ('mia.harris', 'Mia', 'Harris', 'mia@broadcast.com'),
            ('noah.martin', 'Noah', 'Martin', 'noah@broadcast.com'),
            ('olivia.garcia', 'Olivia', 'Garcia', 'olivia@broadcast.com'),
            ('peter.martinez', 'Peter', 'Martinez', 'peter@broadcast.com'),
            ('quinn.robinson', 'Quinn', 'Robinson', 'quinn@broadcast.com'),
            ('rachel.clark', 'Rachel', 'Clark', 'rachel@broadcast.com'),
            ('sam.rodriguez', 'Sam', 'Rodriguez', 'sam@broadcast.com'),
            ('tina.lewis', 'Tina', 'Lewis', 'tina@broadcast.com'),
            ('uma.lee', 'Uma', 'Lee', 'uma@broadcast.com'),
            ('victor.walker', 'Victor', 'Walker', 'victor@broadcast.com'),
            ('wendy.hall', 'Wendy', 'Hall', 'wendy@broadcast.com'),
            ('xander.allen', 'Xander', 'Allen', 'xander@broadcast.com'),
            ('yara.young', 'Yara', 'Young', 'yara@broadcast.com'),
            ('zoe.hernandez', 'Zoe', 'Hernandez', 'zoe@broadcast.com'),
            ('alex.king', 'Alex', 'King', 'alex@broadcast.com'),
            ('bella.wright', 'Bella', 'Wright', 'bella@broadcast.com'),
            ('charlie.lopez', 'Charlie', 'Lopez', 'charlie@broadcast.com'),
            ('diana.hill', 'Diana', 'Hill', 'diana@broadcast.com'),
        ]

        users = {}
        for username, first, last, email in engineers_data:
            u, created = User.objects.get_or_create(
                username=username,
                defaults={'first_name': first, 'last_name': last, 'email': email}
            )
            if created:
                u.set_password('password123')
                u.save()
            users[username] = u
        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} engineers'))

        # ── DEPARTMENTS ─────────────────────────────────────────────────────
        dept_streaming, _ = Department.objects.get_or_create(
            name='Streaming Platform',
            defaults={'description': 'Responsible for all live and on-demand streaming infrastructure and delivery.'}
        )
        dept_data, _ = Department.objects.get_or_create(
            name='Data & Analytics',
            defaults={'description': 'Handles data pipelines, analytics, and business intelligence across Broadcast Company.'}
        )
        dept_mobile, _ = Department.objects.get_or_create(
            name='Mobile & Web',
            defaults={'description': 'Owns all consumer-facing mobile apps and web experiences.'}
        )
        self.stdout.write(self.style.SUCCESS('Created 3 departments'))

        # ── STREAMING PLATFORM TEAMS ─────────────────────────────────────────
        team_cdn, _ = Team.objects.get_or_create(
            name='CDN & Delivery', department=dept_streaming,
            defaults={
                'manager': users['alice.johnson'],
                'description': 'Manages content delivery networks and video delivery optimisation.',
                'mission': 'Deliver broadcast content reliably to millions of viewers worldwide with sub-second latency.',
                'responsibilities': 'CDN configuration, edge caching, ABR ladder management, delivery SLAs.',
                'slack_channel': '#cdn-delivery',
                'email': 'cdn@broadcast.com',
                'status': 'active',
            }
        )
        team_encoder, _ = Team.objects.get_or_create(
            name='Video Encoding', department=dept_streaming,
            defaults={
                'manager': users['bob.smith'],
                'description': 'Builds and maintains video encoding pipelines for live and VOD content.',
                'mission': 'Ensure every broadcast is encoded at the right quality, format, and bitrate.',
                'responsibilities': 'Encoding pipelines, codec research, quality assurance, format support.',
                'slack_channel': '#video-encoding',
                'email': 'encoding@broadcast.com',
                'status': 'active',
            }
        )
        team_player, _ = Team.objects.get_or_create(
            name='Player & Playback', department=dept_streaming,
            defaults={
                'manager': users['carol.white'],
                'description': 'Develops the core video player SDK used across all Broadcast platforms.',
                'mission': 'Deliver a seamless, buffer-free playback experience on every device.',
                'responsibilities': 'Player SDK, DRM integration, accessibility, device support.',
                'slack_channel': '#player-team',
                'email': 'player@broadcast.com',
                'status': 'active',
            }
        )

        # ── DATA & ANALYTICS TEAMS ───────────────────────────────────────────
        team_pipeline, _ = Team.objects.get_or_create(
            name='Data Pipelines', department=dept_data,
            defaults={
                'manager': users['david.brown'],
                'description': 'Builds and operates real-time and batch data ingestion pipelines.',
                'mission': 'Move data reliably from every source to every consumer at scale.',
                'responsibilities': 'Kafka, Spark, Airflow orchestration, data quality monitoring.',
                'slack_channel': '#data-pipelines',
                'email': 'pipelines@broadcast.com',
                'status': 'active',
            }
        )
        team_bi, _ = Team.objects.get_or_create(
            name='Business Intelligence', department=dept_data,
            defaults={
                'manager': users['emma.davis'],
                'description': 'Provides dashboards, reports, and self-service analytics to stakeholders.',
                'mission': 'Enable data-driven decisions at every level of the organisation.',
                'responsibilities': 'Looker dashboards, SQL models, stakeholder reporting, data literacy.',
                'slack_channel': '#bi-team',
                'email': 'bi@broadcast.com',
                'status': 'active',
            }
        )
        team_ml, _ = Team.objects.get_or_create(
            name='ML & Recommendations', department=dept_data,
            defaults={
                'manager': users['frank.miller'],
                'description': 'Trains and deploys machine learning models for personalisation.',
                'mission': 'Surface the right content to the right viewer at the right time.',
                'responsibilities': 'Recommendation engine, A/B testing framework, feature store, model monitoring.',
                'slack_channel': '#ml-recs',
                'email': 'ml@broadcast.com',
                'status': 'active',
            }
        )

        # ── MOBILE & WEB TEAMS ───────────────────────────────────────────────
        team_ios, _ = Team.objects.get_or_create(
            name='iOS App', department=dept_mobile,
            defaults={
                'manager': users['grace.wilson'],
                'description': 'Owns the Broadcast Company iOS application across iPhone and iPad.',
                'mission': 'Build the best live TV experience on Apple devices.',
                'responsibilities': 'Swift development, App Store releases, performance, accessibility.',
                'slack_channel': '#ios-app',
                'email': 'ios@broadcast.com',
                'status': 'active',
            }
        )
        team_android, _ = Team.objects.get_or_create(
            name='Android App', department=dept_mobile,
            defaults={
                'manager': users['henry.moore'],
                'description': 'Builds and maintains the Broadcast Company Android application.',
                'mission': 'Deliver a rich, reliable broadcast experience to Android users.',
                'responsibilities': 'Kotlin development, Play Store releases, fragmentation testing.',
                'slack_channel': '#android-app',
                'email': 'android@broadcast.com',
                'status': 'active',
            }
        )
        team_web, _ = Team.objects.get_or_create(
            name='Web Frontend', department=dept_mobile,
            defaults={
                'manager': users['iris.taylor'],
                'description': 'Develops the broadcast.com web application and progressive web experience.',
                'mission': 'Provide an excellent web viewing experience across all modern browsers.',
                'responsibilities': 'React, TypeScript, accessibility, Core Web Vitals, A/B experiments.',
                'slack_channel': '#web-frontend',
                'email': 'webfe@broadcast.com',
                'status': 'active',
            }
        )
        self.stdout.write(self.style.SUCCESS('Created 9 teams'))

        # ── DEPENDENCIES ─────────────────────────────────────────────────────
        # Player depends on CDN and Encoder
        team_player.upstream_dependencies.set([team_cdn, team_encoder])
        # iOS, Android, Web depend on Player
        team_ios.upstream_dependencies.set([team_player])
        team_android.upstream_dependencies.set([team_player])
        team_web.upstream_dependencies.set([team_player])
        # BI depends on Pipelines; ML depends on Pipelines
        team_bi.upstream_dependencies.set([team_pipeline])
        team_ml.upstream_dependencies.set([team_pipeline])

        # ── MEMBERS ─────────────────────────────────────────────────────────
        def add_members(team, members_info):
            for username, role in members_info:
                TeamMember.objects.get_or_create(
                    team=team, user=users[username],
                    defaults={'join_date': datetime.date(2023, 1, 15)}
                )

        add_members(team_cdn, [
            ('alice.johnson', 'lead'), ('james.anderson', 'senior_engineer'),
            ('kate.thomas', 'engineer'), ('liam.jackson', 'devops'),
            ('mia.harris', 'engineer'), ('noah.martin', 'qa'),
        ])
        add_members(team_encoder, [
            ('bob.smith', 'lead'), ('olivia.garcia', 'senior_engineer'),
            ('peter.martinez', 'engineer'), ('quinn.robinson', 'engineer'),
            ('rachel.clark', 'engineer'),
        ])
        add_members(team_player, [
            ('carol.white', 'lead'), ('sam.rodriguez', 'senior_engineer'),
            ('tina.lewis', 'engineer'), ('uma.lee', 'engineer'),
            ('victor.walker', 'qa'),
        ])
        add_members(team_pipeline, [
            ('david.brown', 'lead'), ('wendy.hall', 'senior_engineer'),
            ('xander.allen', 'engineer'), ('yara.young', 'devops'),
            ('zoe.hernandez', 'engineer'),
        ])
        add_members(team_bi, [
            ('emma.davis', 'lead'), ('alex.king', 'senior_engineer'),
            ('bella.wright', 'engineer'), ('charlie.lopez', 'engineer'),
            ('diana.hill', 'engineer'),
        ])
        add_members(team_ml, [
            ('frank.miller', 'lead'), ('james.anderson', 'architect'),
            ('kate.thomas', 'senior_engineer'), ('liam.jackson', 'engineer'),
            ('mia.harris', 'engineer'),
        ])
        add_members(team_ios, [
            ('grace.wilson', 'lead'), ('noah.martin', 'senior_engineer'),
            ('olivia.garcia', 'engineer'), ('peter.martinez', 'engineer'),
            ('quinn.robinson', 'qa'),
        ])
        add_members(team_android, [
            ('henry.moore', 'lead'), ('rachel.clark', 'senior_engineer'),
            ('sam.rodriguez', 'engineer'), ('tina.lewis', 'engineer'),
            ('uma.lee', 'qa'),
        ])
        add_members(team_web, [
            ('iris.taylor', 'lead'), ('victor.walker', 'senior_engineer'),
            ('wendy.hall', 'engineer'), ('xander.allen', 'engineer'),
            ('yara.young', 'engineer'),
        ])
        self.stdout.write(self.style.SUCCESS('Added team members'))

        # ── REPOSITORIES ─────────────────────────────────────────────────────
        repos = [
            (team_cdn, 'cdn-config', 'https://github.com/broadcast/cdn-config', 'CDN configuration and edge rules'),
            (team_cdn, 'delivery-monitor', 'https://github.com/broadcast/delivery-monitor', 'Real-time delivery monitoring service'),
            (team_encoder, 'encoder-service', 'https://github.com/broadcast/encoder-service', 'Core video encoding service'),
            (team_encoder, 'codec-research', 'https://github.com/broadcast/codec-research', 'Codec evaluation and testing scripts'),
            (team_player, 'player-sdk', 'https://github.com/broadcast/player-sdk', 'Cross-platform video player SDK'),
            (team_player, 'player-web', 'https://github.com/broadcast/player-web', 'Web player implementation'),
            (team_pipeline, 'data-ingest', 'https://github.com/broadcast/data-ingest', 'Kafka-based data ingestion framework'),
            (team_pipeline, 'airflow-dags', 'https://github.com/broadcast/airflow-dags', 'Airflow DAG definitions'),
            (team_bi, 'bi-models', 'https://github.com/broadcast/bi-models', 'dbt models and SQL transformations'),
            (team_ml, 'rec-engine', 'https://github.com/broadcast/rec-engine', 'Recommendation model training and serving'),
            (team_ios, 'ios-app', 'https://github.com/broadcast/ios-app', 'Broadcast iOS app (Swift)'),
            (team_android, 'android-app', 'https://github.com/broadcast/android-app', 'Broadcast Android app (Kotlin)'),
            (team_web, 'web-app', 'https://github.com/broadcast/web-app', 'broadcast.com React frontend'),
        ]
        for team, name, url, desc in repos:
            Repository.objects.get_or_create(team=team, name=name, defaults={'url': url, 'description': desc})
        self.stdout.write(self.style.SUCCESS('Added code repositories'))

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!'))
        self.stdout.write('')
        self.stdout.write('  Admin login → username: admin  |  password: admin123')
        self.stdout.write('  User login  → username: alice.johnson  |  password: password123')
        self.stdout.write('')
        self.stdout.write('  Run the server: python manage.py runserver')
