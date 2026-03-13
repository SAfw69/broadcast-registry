from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from .models import Department, Team, TeamMember, Repository, AuditLog
from .forms import TeamForm, TeamMemberForm, RepositoryForm, DepartmentForm
import json


def home(request):
    departments = Department.objects.annotate(team_count=Count('teams')).order_by('name')
    total_teams = Team.objects.filter(status='active').count()
    total_departments = Department.objects.count()
    total_members = TeamMember.objects.count()
    recent_teams = Team.objects.filter(status='active').order_by('-created_at')[:5]
    context = {
        'departments': departments,
        'total_teams': total_teams,
        'total_departments': total_departments,
        'total_members': total_members,
        'recent_teams': recent_teams,
    }
    return render(request, 'teams/home.html', context)


@login_required
def team_list(request):
    query = request.GET.get('q', '')
    dept_filter = request.GET.get('dept', '')
    status_filter = request.GET.get('status', 'active')

    teams = Team.objects.select_related('department', 'manager').prefetch_related('members')

    if query:
        teams = teams.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(department__name__icontains=query) |
            Q(manager__first_name__icontains=query) |
            Q(manager__last_name__icontains=query)
        )
    if dept_filter:
        teams = teams.filter(department__id=dept_filter)
    if status_filter:
        teams = teams.filter(status=status_filter)

    departments = Department.objects.all()
    view_mode = request.GET.get('view', 'grid')

    context = {
        'teams': teams,
        'departments': departments,
        'query': query,
        'dept_filter': dept_filter,
        'status_filter': status_filter,
        'view_mode': view_mode,
    }
    return render(request, 'teams/team_list.html', context)


@login_required
def team_detail(request, pk):
    team = get_object_or_404(Team.objects.select_related('department', 'manager')
                             .prefetch_related('members__user', 'repositories',
                                               'upstream_dependencies', 'downstream_dependents'), pk=pk)
    context = {'team': team}
    return render(request, 'teams/team_detail.html', context)


@login_required
def team_create(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save()
            AuditLog.objects.create(
                user=request.user,
                action='create',
                model_name='Team',
                object_id=team.id,
                object_repr=str(team),
                ip_address=get_client_ip(request)
            )
            messages.success(request, f'Team "{team.name}" created successfully.')
            return redirect('team_detail', pk=team.pk)
    else:
        form = TeamForm()
    return render(request, 'teams/team_form.html', {'form': form, 'action': 'Create'})


@login_required
def team_edit(request, pk):
    team = get_object_or_404(Team, pk=pk)
    old_repr = str(team)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            team = form.save()
            AuditLog.objects.create(
                user=request.user,
                action='update',
                model_name='Team',
                object_id=team.id,
                object_repr=str(team),
                changes=f'Updated from: {old_repr}',
                ip_address=get_client_ip(request)
            )
            messages.success(request, f'Team "{team.name}" updated successfully.')
            return redirect('team_detail', pk=team.pk)
    else:
        form = TeamForm(instance=team)
    return render(request, 'teams/team_form.html', {'form': form, 'action': 'Edit', 'team': team})


@login_required
def team_delete(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        AuditLog.objects.create(
            user=request.user,
            action='delete',
            model_name='Team',
            object_repr=str(team),
            ip_address=get_client_ip(request)
        )
        team.delete()
        messages.success(request, 'Team disbanded successfully.')
        return redirect('team_list')
    return render(request, 'teams/team_confirm_delete.html', {'team': team})


@login_required
def department_list(request):
    departments = Department.objects.annotate(
        team_count=Count('teams'),
        member_count=Count('teams__members')
    ).order_by('name')
    return render(request, 'teams/department_list.html', {'departments': departments})


@login_required
def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    teams = department.teams.select_related('manager').prefetch_related('members').order_by('name')
    return render(request, 'teams/department_detail.html', {'department': department, 'teams': teams})


@login_required
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            dept = form.save()
            AuditLog.objects.create(
                user=request.user, action='create',
                model_name='Department', object_id=dept.id,
                object_repr=str(dept), ip_address=get_client_ip(request)
            )
            messages.success(request, f'Department "{dept.name}" created.')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'teams/department_form.html', {'form': form, 'action': 'Create'})


@login_required
def department_edit(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=dept)
        if form.is_valid():
            dept = form.save()
            AuditLog.objects.create(
                user=request.user, action='update',
                model_name='Department', object_id=dept.id,
                object_repr=str(dept), ip_address=get_client_ip(request)
            )
            messages.success(request, f'Department "{dept.name}" updated.')
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=dept)
    return render(request, 'teams/department_form.html', {'form': form, 'action': 'Edit', 'dept': dept})


@login_required
def add_member(request, team_pk):
    team = get_object_or_404(Team, pk=team_pk)
    if request.method == 'POST':
        form = TeamMemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.team = team
            member.save()
            AuditLog.objects.create(
                user=request.user, action='update',
                model_name='Team', object_id=team.id,
                object_repr=str(team),
                changes=f'Added member: {member.user.get_full_name()}',
                ip_address=get_client_ip(request)
            )
            messages.success(request, f'{member.user.get_full_name()} added to {team.name}.')
            return redirect('team_detail', pk=team_pk)
    else:
        form = TeamMemberForm()
    return render(request, 'teams/member_form.html', {'form': form, 'team': team})


@login_required
def remove_member(request, team_pk, member_pk):
    team = get_object_or_404(Team, pk=team_pk)
    member = get_object_or_404(TeamMember, pk=member_pk, team=team)
    if request.method == 'POST':
        name = member.user.get_full_name()
        member.delete()
        AuditLog.objects.create(
            user=request.user, action='update',
            model_name='Team', object_id=team.id,
            object_repr=str(team),
            changes=f'Removed member: {name}',
            ip_address=get_client_ip(request)
        )
        messages.success(request, f'{name} removed from {team.name}.')
    return redirect('team_detail', pk=team_pk)


@login_required
def add_repository(request, team_pk):
    team = get_object_or_404(Team, pk=team_pk)
    if request.method == 'POST':
        form = RepositoryForm(request.POST)
        if form.is_valid():
            repo = form.save(commit=False)
            repo.team = team
            repo.save()
            messages.success(request, f'Repository "{repo.name}" added.')
            return redirect('team_detail', pk=team_pk)
    else:
        form = RepositoryForm()
    return render(request, 'teams/repo_form.html', {'form': form, 'team': team})


@login_required
def org_chart(request):
    teams = Team.objects.filter(status='active').select_related('department', 'manager').prefetch_related('upstream_dependencies')
    departments = Department.objects.prefetch_related('teams').all()

    # Build JSON for D3.js visualization
    nodes = []
    edges = []
    for team in teams:
        nodes.append({
            'id': team.id,
            'name': team.name,
            'department': team.department.name,
            'manager': team.manager.get_full_name() if team.manager else 'N/A',
            'member_count': team.members.count(),
        })
        for dep in team.upstream_dependencies.all():
            edges.append({'source': dep.id, 'target': team.id})

    context = {
        'departments': departments,
        'nodes_json': json.dumps(nodes),
        'edges_json': json.dumps(edges),
    }
    return render(request, 'teams/org_chart.html', context)


@login_required
def audit_log(request):
    logs = AuditLog.objects.select_related('user').order_by('-timestamp')[:200]
    return render(request, 'teams/audit_log.html', {'logs': logs})


@login_required
def search(request):
    query = request.GET.get('q', '')
    teams = []
    departments = []
    if query:
        teams = Team.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).select_related('department')[:10]
        departments = Department.objects.filter(name__icontains=query)[:5]
    context = {'query': query, 'teams': teams, 'departments': departments}
    return render(request, 'teams/search_results.html', context)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')
