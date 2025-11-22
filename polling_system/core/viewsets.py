from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
# ✅ ADDED IsAuthenticated here
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from django.db import transaction
from .models import Project, ProjectImage, Criteria, Vote, Rating, Comment
from .serializers import (
    ProjectListSerializer, ProjectDetailSerializer,
    ProjectImageSerializer, RatingSerializer,
    CommentSerializer, CriteriaSerializer
)
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(status="published").select_related("creator").prefetch_related("images", "votes")
    
    # Default rule: Owners can edit, others can only read
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["category", "is_featured"]
    ordering_fields = ["created_at", "vote_count", "average_score"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProjectDetailSerializer
        return ProjectListSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user, status="published")

    # ✅ FIX: Added permission_classes=[IsAuthenticated] to allow ANY logged-in user to vote
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def vote(self, request, pk=None):
        project = self.get_object()
        vote, created = Vote.objects.get_or_create(user=request.user, project=project)
        
        if not created:
            return Response({"detail": "Already voted"}, status=status.HTTP_400_BAD_REQUEST)

        # Count directly from DB
        project.vote_count = Vote.objects.filter(project=project).count()
        project.save(update_fields=["vote_count"])

        return Response({"detail": "Voted successfully"}, status=status.HTTP_201_CREATED)

    # ✅ FIX: Added permission_classes=[IsAuthenticated] here too
    @action(detail=True, methods=["delete"], permission_classes=[IsAuthenticated])
    def unvote(self, request, pk=None):
        project = self.get_object()
        deleted, _ = Vote.objects.filter(user=request.user, project=project).delete()
        
        if deleted == 0:
            return Response({"detail": "Not voted"}, status=status.HTTP_400_BAD_REQUEST)

        # Count directly from DB
        project.vote_count = Vote.objects.filter(project=project).count()
        project.save(update_fields=["vote_count"])

        return Response({"detail": "Vote removed"}, status=status.HTTP_204_NO_CONTENT)


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
        return Rating.objects.filter(project_id=self.kwargs["project_pk"], user=self.request.user)

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs["project_pk"])
        with transaction.atomic():
            serializer.save(user=self.request.user, project=project)


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