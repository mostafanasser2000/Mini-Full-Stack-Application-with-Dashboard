from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.http.response import JsonResponse
from .filters import MedicationFilter, RefillRequestFilter
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from .serializers import (
    CategorySerializer,
    MedicationSerializer,
    RefillRequestSerializer,
)
from .permissions import IsAdminOrReadOnly, RefillRequestPermission
from .models import Category, Medication, RefillRequest, MEDICATION_FORMS_CHOICES


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    lookup_field = "slug"
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    search_fields = ["name"]


class MedicationViewSet(ModelViewSet):
    queryset = Medication.objects.select_related("category")
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = MedicationSerializer
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = "slug"

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = MedicationFilter
    search_fields = [
        "name",
    ]
    ordering_fields = ["price", "quantity"]

    def perform_update(self, serializer):
        image = self.request.FILES.get("image")
        if image:
            serializer.validated_data["image"] = image
        else:
            if not hasattr(serializer.instance, "image"):
                serializer.validated_data.pop("image", None)
        super().perform_update(serializer)


class RefillRequestViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, RefillRequestPermission]
    serializer_class = RefillRequestSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = RefillRequestFilter
    search_fields = ["medication__name"]
    ordering_fields = ["approved_at", "quantity"]

    def destroy(self, request, *args, **kwargs):
        refill_request = self.get_object()
        if refill_request.status != "pending":
            return Response(
                {"detail": "Can not delete requests that is approved or rejected"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        qs = RefillRequest.objects.select_related("user", "medication")
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        """ "Approve a pending request by admins"""
        refill_request = self.get_object()
        if refill_request.status != "pending":
            return Response(
                {"detail": "Only pending requests can be approved."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        refill_request.approve()

        return Response(
            {"detail": f"Refill request ({refill_request.id}) has been approved."},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        """ "Reject a pending request by admins"""
        refill_request = self.get_object()
        if refill_request.status != "pending":
            return Response(
                {"detail": "Only pending requests can be rejected."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        refill_request.reject()
        return Response(
            {"detail": f"Refill request ({refill_request.id}) has been rejected."},
            status=status.HTTP_200_OK,
        )


@api_view(
    [
        "GET",
    ]
)
@renderer_classes((JSONRenderer,))
def medication_forms(request):
    return Response(data=MEDICATION_FORMS_CHOICES)
