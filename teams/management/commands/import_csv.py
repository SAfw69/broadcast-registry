import csv
import logging
from django.core.management.base import BaseCommand
from teams.models import Department, Team

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Imports Departments and Teams from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='The path to the CSV file to be imported')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file_path']
        
        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                required_fields = ['department_name', 'team_name']
                if not reader.fieldnames or not all(field in reader.fieldnames for field in required_fields):
                    self.stderr.write(self.style.ERROR(f"CSV must contain at least the following columns: {', '.join(required_fields)}"))
                    return

                teams_created = 0
                depts_created = 0

                for row_num, row in enumerate(reader, start=2):
                    dept_name = row.get('department_name', '').strip()
                    dept_desc = row.get('department_description', '').strip()
                    
                    if not dept_name:
                        self.stderr.write(self.style.WARNING(f"Row {row_num}: Skipping row with empty department_name"))
                        continue

                    dept, created = Department.objects.get_or_create(
                        name=dept_name,
                        defaults={'description': dept_desc}
                    )
                    if created:
                        depts_created += 1

                    team_name = row.get('team_name', '').strip()
                    if team_name:
                        team_desc = row.get('team_description', '').strip()
                        mission = row.get('mission', '').strip()
                        slack = row.get('slack_channel', '').strip()
                        email = row.get('email', '').strip()
                        status = row.get('status', 'active').strip().lower()

                        # Ensure status is valid
                        valid_statuses = [choice[0] for choice in Team.STATUS_CHOICES]
                        if status not in valid_statuses:
                            status = 'active'

                        team, t_created = Team.objects.update_or_create(
                            name=team_name,
                            department=dept,
                            defaults={
                                'description': team_desc,
                                'mission': mission,
                                'slack_channel': slack,
                                'email': email,
                                'status': status
                            }
                        )
                        if t_created:
                            teams_created += 1

                self.stdout.write(self.style.SUCCESS(f"Successfully processed CSV. Created {depts_created} Departments and {teams_created} Teams."))
                
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File not found: {csv_file_path}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred while parsing the CSV: {str(e)}"))
