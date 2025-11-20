from django.contrib import admin
from .models import Project, Criteria, Rating, Comment

# This tells the Admin Panel to show the Project table
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

# This shows the Criteria table
@admin.register(Criteria)
class CriteriaAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

# This shows the Ratings table with useful columns
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('project', 'criteria', 'score', 'user')
    list_filter = ('project', 'criteria') # Adds sidebar filters

# This shows the Comments
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'created_at')
