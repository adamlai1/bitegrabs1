from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Group, GroupMember
from .forms import GroupForm, InviteMemberForm, GroupMemberForm
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
import uuid


@login_required
def home(request):
    return render(request, 'home.html')
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.leader = request.user
            group.save()

            # Add the leader as a member of the group
            GroupMember.objects.create(group=group, user=request.user)

            return redirect('group_detail', group_id=group.id)
    else:
        form = GroupForm()
    return render(request, 'groups/create_group.html', {'form': form})

def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    members = GroupMember.objects.filter(group=group)

    leader_name = group.leader.username if group.leader else group.guest_leader
    invitation_link = request.build_absolute_uri(reverse('join_group', args=[group.token]))

    # Check if the logged-in user is a member
    is_member = members.filter(user=request.user).exists()

    return render(request, 'groups/group_detail.html', {
        'group': group,
        'members': members,
        'leader_name': leader_name,
        'invitation_link': invitation_link,
        'is_member': is_member,
    })
def invite_member(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = InviteMemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.group = group
            member.save()
            return redirect('group_detail', group_id=group.id)
    else:
        form = InviteMemberForm()
    return render(request, 'groups/invite_member.html', {'form': form, 'group': group})


def submit_preferences(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.user.is_authenticated:
        # For logged-in users
        member = get_object_or_404(GroupMember, group=group, user=request.user)
    else:
        # For guests
        guest_name = request.session.get('guest_name')
        if not guest_name:
            return redirect('enter_guest_name', token=group.token)
        member = get_object_or_404(GroupMember, group=group, guest_name=guest_name)

    if request.method == 'POST':
        form = GroupMemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('group_detail', group_id=group.id)
    else:
        form = GroupMemberForm(instance=member)

    return render(request, 'groups/submit_preferences.html', {'form': form, 'group': group})
def calculate_best_spot(group):
    # Placeholder logic for calculating the best food spot
    # Implement your algorithm here
    return "Sample Best Food Spot"


def submit_guest_preferences(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    guest_name = request.session.get('guest_name')

    if request.method == 'POST':
        form = GroupMemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.group = group
            member.guest_name = guest_name
            member.save()
            return redirect('group_detail', group_id=group.id)
    else:
        form = GroupMemberForm()

    return render(request, 'groups/submit_preferences.html', {'form': form, 'group': group})


from django.shortcuts import get_object_or_404


def join_group(request, token):
    group = get_object_or_404(Group, token=token)

    if request.method == 'POST':
        if 'login' in request.POST:
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('group_detail', group_id=group.pk)  # Use 'group_id' here
        elif 'join_as_guest' in request.POST:
            guest_name = request.POST.get('guest_name')
            if guest_name:
                GroupMember.objects.create(group=group, guest_name=guest_name)
                return redirect('group_detail', group_id=group.pk)  # Use 'group_id' here
    else:
        form = AuthenticationForm()

    return render(request, 'groups/join_group.html', {'group': group, 'form': form})
def enter_guest_name(request, token):
    if request.method == 'POST':
        guest_name = request.POST.get('guest_name')
        request.session['guest_name'] = guest_name
        return redirect('join_group', token=token)
    return render(request, 'groups/enter_guest_name.html', {'token': token})
def kick_member(request, group_id, user_id):
    group = get_object_or_404(Group, pk=group_id)
    user_to_remove = get_object_or_404(User, pk=user_id)

    # Check if the request.user is the leader of the group
    if request.user != group.leader:
        return HttpResponseForbidden("You are not allowed to perform this action.")

    # Remove the user from the group
    GroupMembership.objects.filter(group=group, user=user_to_remove).delete()

    return redirect('group_detail', group_id=group.pk)