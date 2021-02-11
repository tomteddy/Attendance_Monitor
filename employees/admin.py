from django.contrib import admin
from .models import User, Employee, Company, Work_log
# Register your models here.


admin.site.register(User)
admin.site.register(Employee)
admin.site.register(Company)
admin.site.register(Work_log)