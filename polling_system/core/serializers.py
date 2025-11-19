# core/serializers.py
from rest_framework import serializers
from .models import Project, ProjectImage, Criteria, Vote, Rating, Comment


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ["id", "image", "caption", "order"]


class CriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criteria
        fields = ["id", "name", "description", "weight"]


class RatingSerializer(serializers.ModelSerializer):
    criteria = CriteriaSerializer(read_only=True)
    criteria_id = serializers.PrimaryKeyRelatedField(
        queryset=Criteria.objects.all(), source="criteria", write_only=True
    )

    class Meta:
        model = Rating
        fields = ["id", "criteria", "criteria_id", "score", "created_at"]
        read_only_fields = ["created_at"]

    def validate(self, attrs):
        project = self.context["project"]
        criteria = attrs["criteria"]
        if criteria.project_category != project.category:
            raise serializers.ValidationError(
                f"Criteria '{criteria}' does not apply to {project.get_category_display()} projects"
            )
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "content", "created_at", "updated_at", "parent", "replies"]
        read_only_fields = ["user", "created_at", "updated_at"]

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True, context=self.context).data
        return []


class ProjectListSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    category_display = serializers.CharField(source="get_category_display", read_only=True)
    has_voted = serializers.SerializerMethodField()
    has_rated = serializers.SerializerMethodField()
    images = ProjectImageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id", "name", "description", "category", "category_display",
            "creator", "status", "is_featured", "created_at",
            "vote_count", "average_score", "rating_count",
            "has_voted", "has_rated", "images"
        ]

    def get_has_voted(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return obj.votes.filter(user=user).exists()
        return False

    def get_has_rated(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return obj.ratings.filter(user=user).exists()
        return False


class ProjectDetailSerializer(ProjectListSerializer):
    ratings = RatingSerializer(many=True, read_only=True)
    criteria = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta(ProjectListSerializer.Meta):
        fields = ProjectListSerializer.Meta.fields + ["ratings", "criteria", "comments"]

    def get_criteria(self, obj):
        criteria = Criteria.objects.filter(project_category=obj.category)
        return CriteriaSerializer(criteria, many=True).data