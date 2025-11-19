# core/viewsets.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
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

    @action(detail=True, methods=["post"])
    def vote(self, request, pk=None):
        project = self.get_object()
        vote, created = Vote.objects.get_or_create(user=request.user, project=project)
        if not created:
            return Response({"detail": "Already voted"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Voted successfully"}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete"])
    def unvote(self, request, pk=None):
        project = self.get_object()
        vote = Vote.objects.filter(user=request.user, project=project).delete()
        if vote[0] == 0:
            return Response({"detail": "Not voted"}, status=status.HTTP_400_BAD_REQUEST)
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