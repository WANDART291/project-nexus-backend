from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.db.models import Avg
from django.core.cache import cache


from .models import Project, ProjectImage, Criteria, Vote, Rating, Comment
from .serializers import (
    ProjectListSerializer, ProjectDetailSerializer,
    ProjectImageSerializer, RatingSerializer,
    CommentSerializer, CriteriaSerializer
)
from .permissions import IsOwnerOrReadOnly

from .tasks import send_rating_email 

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class ProjectViewSet(viewsets.ModelViewSet):
   
    queryset = Project.objects.filter(status="published").select_related("creator").prefetch_related("images", "votes", "ratings")
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["category", "is_featured"]
    ordering_fields = ["created_at", "vote_count"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProjectDetailSerializer
        return ProjectListSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user, status="published")

    @action(detail=False, methods=['get'])
    def top(self, request):
      
        cached_data = cache.get("leaderboard")
        if cached_data:
            return Response(cached_data)

        top_projects = self.get_queryset().annotate(
            avg_rating=Avg('ratings__score')
        ).order_by('-avg_rating')
        
        serializer = self.get_serializer(top_projects, many=True)
        data = serializer.data

        cache.set("leaderboard", data, 300)
        return Response(data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def vote(self, request, pk=None):
        project = self.get_object()
        user = request.user
        
    
        if 'score' in request.data:
            criteria_id = request.data.get('criteria_id', 1)
            try:
                criteria = Criteria.objects.get(id=criteria_id)
            except Criteria.DoesNotExist:
            
                criteria, _ = Criteria.objects.get_or_create(name="General", id=1)
            
            Rating.objects.update_or_create(
                user=user, project=project, criteria=criteria,
                defaults={'score': request.data['score']}
            )
            return Response({"detail": "Voted successfully"}, status=status.HTTP_201_CREATED)

        
        else:
            vote, created = Vote.objects.get_or_create(user=user, project=project)
            if not created:
                return Response({"detail": "Already voted"}, status=status.HTTP_400_BAD_REQUEST)
            
            project.vote_count = Vote.objects.filter(project=project).count()
            project.save(update_fields=["vote_count"])
            return Response({"detail": "Voted successfully"}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete", "post"], permission_classes=[IsAuthenticated])
    def unvote(self, request, pk=None):
        project = self.get_object()
        user = request.user

        
        deleted_votes, _ = Vote.objects.filter(user=user, project=project).delete()

        deleted_ratings, _ = Rating.objects.filter(user=user, project=project).delete()

  
        if deleted_votes > 0 or deleted_ratings > 0:
            
            project.vote_count = Vote.objects.filter(project=project).count()
            project.save(update_fields=["vote_count"])
            return Response({"detail": "Vote removed"}, status=status.HTTP_200_OK)
        
        return Response({"detail": "Not voted"}, status=status.HTTP_400_BAD_REQUEST)


class ProjectImageViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectImageSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return ProjectImage.objects.filter(project_id=self.kwargs["project_pk"])

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs["project_pk"])
        serializer.save(project=project)


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Rating.objects.filter(project_id=self.kwargs["project_pk"], user=self.request.user)
        return Rating.objects.none()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if "project_pk" in self.kwargs:
            context["project"] = Project.objects.get(pk=self.kwargs["project_pk"])
        return context

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs["project_pk"])
        try:
            with transaction.atomic():
                serializer.save(user=self.request.user, project=project)
                # Check if email task exists and user has email
                if hasattr(project, 'creator') and project.creator and project.creator.email:
                    send_rating_email.delay(project.creator.email, project.name)
        except IntegrityError:
            raise ValidationError({"detail": "You have already rated this project."})


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(project_id=self.kwargs["project_pk"], parent=None)

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs["project_pk"])
        serializer.save(user=self.request.user, project=project)


class CriteriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Criteria.objects.all()
    serializer_class = CriteriaSerializer
    permission_classes = [AllowAny]