from django.urls import path
from .views import (
    login_view,
    register_view,
    manager_dashboard_view,
    approver_dashboard_view,
    user_dashboard_view,
    logout_view,
    contract_list_ui,
    add_contract,
    contract_detail,
    edit_contract,
    delete_contract,
    download_contract_document,
    manage_clauses,
    delete_clause,
    create_modification_request,
    user_modification_list,
    user_list,
    add_user,
    edit_user,
    delete_user,
    user_detail,
    approve_contract,
    reject_contract,
    document_list,
    approval_queue_view,          
    approval_history_view,        
    my_profile_view,                        
    version_history_view,   
    edit_profile_view,
    help_support_view,      
    admin_dashboard_view,    
    audit_logs_view,
)

urlpatterns = [
    # Auth & Role-Based Dashboard Routes
    path('', login_view, name='login'),
    path('login/', login_view, name='login_page'),
    path('register/', register_view, name='register'),
    path('documents/', document_list, name='document_list'), 
    path('logout/', logout_view, name='logout'),
    
    path('dashboard/', manager_dashboard_view, name='dashboard'),
    path('manager-dashboard/', manager_dashboard_view, name='manager_dashboard'),
    path('approver-dashboard/', approver_dashboard_view, name='approver_dashboard'),
    path('user-dashboard/', user_dashboard_view, name='user_dashboard'),

    # Contract Operations UI
    path('contracts/', contract_list_ui, name='contract_list'),
    path('contracts/add/', add_contract, name='add_contract'),
    path('contracts/<int:pk>/', contract_detail, name='contract_detail'),
    path('contracts/edit/<int:pk>/', edit_contract, name='edit_contract'),
    path('contracts/delete/<int:pk>/', delete_contract, name='delete_contract'),

    # Approver Actions for Contracts
    path('approvals/approve/<int:pk>/', approve_contract, name='approve_contract'),
    path('approvals/reject/<int:pk>/', reject_contract, name='reject_contract'),
    path('approval-queue/', approval_queue_view, name='approval_queue'),
    path('approval-history/', approval_history_view, name='approval_history'),

    # Document, Clause & Modification Management Routes
    path('contract/<int:contract_id>/download/', download_contract_document, name='download_contract_document'),
    path('contract/<int:contract_id>/clauses/', manage_clauses, name='manage_clauses'),
    path('clause/<int:clause_id>/delete/', delete_clause, name='delete_clause'),
    path('contract/<int:contract_id>/request-modification/', create_modification_request, name='create_modification_request'),
    path('my-modifications/', user_modification_list, name='user_modification_list'),
    
    # Version History Route Added
    path('version-history/', version_history_view, name='version_history'),  

    # Admin User & Role Management Routes
    path('users/', user_list, name='user_list'),
    path('users/add/', add_user, name='add_user'),  
    path('users/edit/<int:user_id>/', edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', delete_user, name='user_delete'), 
    path('users/<int:user_id>/', user_detail, name='user_detail'),
    
    # My Profile Route Added
    path('my-profile/', my_profile_view, name='my_profile'),
    path('my-profile/edit/', edit_profile_view, name='edit_profile'),

    # Help & Support Route
    path('help-support/', help_support_view, name='help_support'),
    
    # Admin Dashboard Route
    path('admin-dashboard/', admin_dashboard_view, name='admin_dashboard'),
    
    path('audit-logs/', audit_logs_view, name='audit_logs'),
    
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
]