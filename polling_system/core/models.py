# core/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Count
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Project(models.Model):
    CATEGORY_CHOICES = [
        ("poll", "Online Polling"),
        ("movie", "Movie Recommendation"),
        ("ecommerce", "E-commerce Catalogue"),
        ("social", "Social Feed"),
        ("job", "Job Platform"),
    ]

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
        ("under_review", "Under Review"),
        ("rejected", "Rejected"),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(
        'User', on_delete=models.SET_NULL, null=True, related_name="created_projects"
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="poll")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Cached stats
    vote_count = models.PositiveIntegerField(default=0, editable=False)
    average_score = models.FloatField(null=True, blank=True, editable=False, db_index=True)
    rating_count = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["category", "status"]),
            models.Index(fields=["-vote_count"]),
            models.Index(fields=["-average_score"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return f"{self.name} by {self.creator}"

    def recalculate_stats(self):
        agg = self.ratings.aggregate(avg=Avg("score"), count=Count("id"))
        self.average_score = round(agg["avg"] or 0, 2)
        self.rating_count = agg["count"] or 0
        self.vote_count = self.votes.count()
        self.save(update_fields=["average_score", "rating_count", "vote_count"])


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="projects/%Y/%m/%d/")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]


class Criteria(models.Model):
    project_category = models.CharField(max_length=20, choices=Project.CATEGORY_CHOICES)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    weight = models.PositiveSmallIntegerField(default=1)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ("project_category", "name")
        ordering = ["project_category", "order"]

    def __str__(self):
        return f"[{self.get_project_category_display()}] {self.name}"


class Vote(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="votes")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="votes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "project")


class Rating(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="ratings")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="ratings")
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE, related_name="ratings")
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "project", "criteria")
        indexes = [models.Index(fields=["project", "criteria"])]

    def clean(self):
        if self.project.category != self.criteria.project_category:
            from django.core.exceptions import ValidationError
            raise ValidationError("Criteria does not match project category")


class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="comments")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["project", "-created_at"])]


# Signals
@receiver([post_save, post_delete], sender=Vote)
@receiver([post_save, post_delete], sender=Rating)
def update_project_stats(sender, instance, **kwargs):
    if isinstance(instance, Vote):
        instance.project.recalculate_stats()
    elif isinstance(instance, Rating):
        instance.project.recalculate_stats()
