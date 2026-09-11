from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import AuditLog  # किंवा तुमचा मॉडेल ज्या फाईलमध्ये असेल त्यावरून इम्पोर्ट करा

def is_admin(user):
    # जर चुकून request आलीच तर user मध्ये रूपांतर करा
    if hasattr(user, 'user'):
        user = user.user
    return user.is_superuser or user.groups.filter(name='Admin').exists() or user.username.lower() == 'admin'
# --- DASHBOARD VIEWS ---

@login_required
def admin_dashboard_view(request):
    """Admin Dashboard View"""
    if not (request.user.is_superuser or request.user.username.lower() == 'admin'):
        messages.error(request, "Unauthorized action.")
        return redirect('user_dashboard')
        
    total_users = User.objects.count()
    total_contracts = 3  # तुमच्या कॉन्ट्रॅक्ट्स मॉडेलनुसार count() लावू शकता
    audit_logs = AuditLog.objects.all().order_by('-timestamp')[:5]  # शेवटचे ५ लॉग्स
    
    context = {
        'total_users': total_users,
        'total_contracts': total_contracts,
        'audit_logs': audit_logs,
    }
    return render(request, 'users/admin_dashboard.html', context)
@login_required
def manager_dashboard_view(request):
    """Manager dashboard view."""
    return render(request, 'users/manager_dashboard.html')

@login_required
def approver_dashboard_view(request):
    """Approver dashboard view."""
    return render(request, 'users/approver_dashboard.html')

@login_required
def user_dashboard_view(request):
    """Standard user dashboard view."""
    return render(request, 'users/user_dashboard.html')


# --- USER MANAGEMENT VIEWS ---

@login_required
def user_list(request):
    """List system users and fetch groups for the modal dropdown."""
    if not is_admin(request):
        messages.error(request, "Access denied.")
        return redirect('user_dashboard')
        
    users = User.objects.all().order_by('-id')
    groups = Group.objects.all()
    return render(request, 'users/user_list.html', {'users': users, 'groups': groups})

@login_required
def add_user(request):
    """Handle new user creation (POST) from the modal with role assignment."""
    if not is_admin(request):
        messages.error(request, "Unauthorized action.")
        return redirect('user_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        full_name = request.POST.get('full_name', '')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role_id = request.POST.get('role')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('user_list')
        
        if not password:
            password = 'defaultpassword123'
            
        user = User.objects.create_user(username=username, email=email, password=password)
        
        if full_name:
            name_parts = full_name.split(' ', 1)
            user.first_name = name_parts[0]
            user.last_name = name_parts[1] if len(name_parts) > 1 else ''
            
        if role_id:
            try:
                group = Group.objects.get(id=role_id)
                user.groups.add(group)
            except Group.DoesNotExist:
                pass
                
        user.save()
        messages.success(request, f'User {username} created successfully!')
        return redirect('user_list')
        
    return redirect('user_list')

@login_required
def edit_user(request, user_id):
    """Handle editing an existing user, including role, status, and credentials."""
    if not is_admin(request):
        messages.error(request, "Unauthorized action.")
        return redirect('user_dashboard')

    user_obj = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        role_id = request.POST.get('role')
        is_active = request.POST.get('is_active') == 'on'
        new_password = request.POST.get('password')
        
        if username:
            user_obj.username = username
        user_obj.email = email
        user_obj.is_active = is_active
        
        if new_password:
            user_obj.set_password(new_password)
            
        user_obj.save()
        
        user_obj.groups.clear()
        if role_id:
            try:
                group = Group.objects.get(id=role_id)
                user_obj.groups.add(group)
            except Group.DoesNotExist:
                pass
                
        messages.success(request, 'User updated successfully!')
        return redirect('user_list')
        
    groups = Group.objects.all()
    return render(request, 'users/edit_user.html', {'edit_user': user_obj, 'groups': groups})

@login_required
def user_detail(request, user_id):
    """View detailed information about a specific user."""
    if not is_admin(request):
        messages.error(request, "Unauthorized action.")
        return redirect('user_dashboard')
        
    user_obj = get_object_or_404(User, pk=user_id)
    
    # इथे HttpResponse ऐवजी templates/users/user_detail.html रेंडर करा
    return render(request, 'users/user_detail.html', {'user_obj': user_obj})

@login_required
def delete_user(request, user_id):
    """Delete a system user."""
    if not is_admin(request):
        messages.error(request, "Unauthorized action.")
        return redirect('user_dashboard')
        
    user_obj = get_object_or_404(User, pk=user_id)
    if user_obj.is_superuser:
        messages.error(request, "Superuser accounts cannot be deleted.")
        return redirect('user_list')
        
    username = user_obj.username
    user_obj.delete()
    messages.success(request, f"User '{username}' deleted successfully.")
    return redirect('user_list')


# --- PROFILE & MISC VIEWS ---

@login_required
def my_profile_view(request):
    """Allows currently logged-in user to view profile info."""
    return render(request, 'users/my_profile.html')

@login_required
def edit_profile_view(request):
    """Allows currently logged-in user to update their basic profile info."""
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()
        messages.success(request, "Your profile has been updated successfully.")
        return redirect('my_profile')
        
    return render(request, 'users/edit_profile.html')

@login_required
def help_support_view(request):
    """Help and Support view."""
    return render(request, 'users/help_support.html')

@login_required
def version_history_view(request):
    """Version history view."""
    return render(request, 'users/version_history.html')


# --- CONTRACT & DOCUMENT MANAGEMENT PLACEHOLDER VIEWS ---

@login_required
def document_list(request):
    return render(request, 'contracts/document_list.html')

@login_required
def contract_list_ui(request):
    return render(request, 'contracts/contract_list.html')

@login_required
def add_contract(request):
    return render(request, 'contracts/add_contract.html')

@login_required
def contract_detail(request, pk):
    return render(request, 'contracts/contract_detail.html')

@login_required
def edit_contract(request, pk):
    return render(request, 'contracts/edit_contract.html')

@login_required
def delete_contract(request, pk):
    return redirect('contract_list')

@login_required
def approve_contract(request, pk):
    return redirect('approval_queue')

@login_required
def reject_contract(request, pk):
    return redirect('approval_queue')

@login_required
def approval_queue_view(request):
    return render(request, 'contracts/approval_queue.html')

@login_required
def approval_history_view(request):
    return render(request, 'contracts/approval_history.html')

@login_required
def download_contract_document(request, contract_id):
    return redirect('contract_list')

@login_required
def manage_clauses(request, contract_id):
    return render(request, 'contracts/manage_clauses.html')

@login_required
def delete_clause(request, clause_id):
    return redirect('contract_list')

@login_required
def create_modification_request(request, contract_id):
    return redirect('contract_list')

@login_required
def user_modification_list(request):
    return render(request, 'contracts/user_modification_list.html')


# --- AUTHENTICATION VIEWS ---

def login_view(request):
    """Handle user login and role-based redirection."""
    if request.method == 'POST':
        u_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        
        user = authenticate(request, username=u_name, password=pass_word)
        if user is not None:
            login(request, user)
            if user.is_superuser or u_name.lower() == 'admin':
                return redirect('admin_dashboard')
            elif user.groups.filter(name='Manager').exists() or user.is_staff or u_name.lower() == 'manager':
                return redirect('manager_dashboard')
            elif user.groups.filter(name='Approver').exists() or u_name.lower() == 'approver':
                return redirect('approver_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password!'})
            
    return render(request, 'login.html')

def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect('login')

def register_view(request):
    """Handle user registration."""
    if request.method == 'POST':
        u_name = request.POST.get('username')
        email = request.POST.get('email')
        pass_word = request.POST.get('password')
        
        if User.objects.filter(username=u_name).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'register.html')
            
        user = User.objects.create_user(username=u_name, email=email, password=pass_word)
        user.save()
        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('login')
        
    return render(request, 'register.html')

@login_required
def audit_logs_view(request):
    if not (request.user.is_superuser or request.user.username.lower() == 'admin'):
        messages.error(request, "Unauthorized action.")
        return redirect('user_dashboard')
    
    # डेटाबेसमधून लॉग्ज फेच करणे (नवीन सर्वात आधी)
    logs = AuditLog.objects.all().order_by('-timestamp') 
    return render(request, 'users/audit_logs.html', {'logs': logs})