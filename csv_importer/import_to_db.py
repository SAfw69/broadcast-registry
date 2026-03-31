import os
import sys
import csv
import django

# Add the project root to the Python path so Django can find the settings module
# The script is in csv_importer/, so the project root is one level up
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'broadcast_registry.settings')
django.setup()

# Now we can import Django models
from teams.models import Department, Team

def main(csv_file_path):
    print(f"Starting import from {csv_file_path}...")
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            required_fields = ['department_name', 'team_name']
            if not reader.fieldnames or not all(field in reader.fieldnames for field in required_fields):
                print(f"Error: CSV must contain at least the following columns: {', '.join(required_fields)}")
                return

            teams_created = 0
            depts_created = 0

            for row_num, row in enumerate(reader, start=2):
                dept_name = row.get('department_name', '').strip()
                dept_desc = row.get('department_description', '').strip()
                
                if not dept_name:
                    print(f"Row {row_num}: Skipping row with empty department_name")
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

            print(f"Success! Created {depts_created} Departments and {teams_created} Teams.")
            
    except FileNotFoundError:
        print(f"Error: File not found: {csv_file_path}")
    except Exception as e:
        print(f"An error occurred while parsing the CSV: {str(e)}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python import_to_db.py <path_to_csv>")
        sys.exit(1)
    
    main(sys.argv[1])
