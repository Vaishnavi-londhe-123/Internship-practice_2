from django.contrib import admin
from .models import (
    Contract, Document, Clause, 
    Modification, Approval, Version, AuditLog
)

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('contract_name', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('contract_name', 'description')

@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('contract', 'version_number', 'modified_by', 'created_at')

admin.site.register(Document)
admin.site.register(Clause)
admin.site.register(Modification)
admin.site.register(Approval)
admin.site.register(AuditLog)