from django.db import models
from django.contrib.auth.models import User

# 1. CONTRACT ENTITY
class Contract(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('UNDER_REVIEW', 'Under Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    contract_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='contracts/', null=True, blank=True)
    
    # Error fix karnyasathi ha approver field null=True ani blank=True sobat add kela ahe
    approver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_contracts'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='DRAFT'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_contracts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.contract_name


# 2. DOCUMENT ENTITY
class Document(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='documents')
    file_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='contracts_docs/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name


# 3. CLAUSE ENTITY
class Clause(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='clauses')
    clause_number = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=255)
    text_content = models.TextField()
    order_number = models.PositiveIntegerField(default=1)  
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order_number']  

    def __str__(self):
        return f"{self.order_number}. {self.title}"


# 4. MODIFICATION ENTITY
class Modification(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='modifications', null=True, blank=True)
    clause = models.ForeignKey(Clause, on_delete=models.SET_NULL, null=True, blank=True, related_name='modifications')
    original_value = models.TextField(blank=True, null=True)
    proposed_modification = models.TextField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Modification by {self.modified_by.username} - Status: {self.status}"

# Alias for compatibility
ModificationRequest = Modification


# 5. APPROVAL ENTITY
class Approval(models.Model):
    APPROVAL_STATUS = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='approvals')
    
    approver = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_approvals'
    )
    
    status = models.CharField(max_length=20, choices=APPROVAL_STATUS, default='PENDING')
    comments = models.TextField(blank=True, null=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Approval for {self.contract.contract_name} - {self.status}"

# 6. VERSION ENTITY
class Version(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='versions')
    version_number = models.PositiveIntegerField()
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='contract_versions/', null=True, blank=True)
    change_description = models.TextField(blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contract.contract_name} - Version {self.version_number}"


# 7. AUDIT LOG ENTITY
class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)  # <--- इथे फक्त एकच वेळेस proper field ठेव
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.action} at {self.timestamp}"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"    