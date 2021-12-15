from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from adventure import models, notifiers, repositories, serializers, usecases


class CreateVehicleAPIView(APIView):
    def post(self, request: Request) -> Response:
        payload = request.data
        vehicle_type = models.VehicleType.objects.get(
            name=payload["vehicle_type"])
        vehicle = models.Vehicle.objects.create(
            name=payload["name"],
            passengers=payload["passengers"],
            vehicle_type=vehicle_type,
        )
        return Response(
            {
                "id": vehicle.id,
                "name": vehicle.name,
                "passengers": vehicle.passengers,
                "vehicle_type": vehicle.vehicle_type.name,
            },
            status=201,
        )


class StartJourneyAPIView(generics.CreateAPIView):
    serializer_class = serializers.JourneySerializer

    def perform_create(self, serializer) -> None:
        repo = self.get_repository()
        notifier = notifiers.Notifier()
        usecase = usecases.StartJourney(repo, notifier).set_params(
            serializer.validated_data
        )
        try:
            usecase.execute()
        except usecases.StartJourney.CantStart as e:
            raise ValidationError({"detail": str(e)})

    def get_repository(self) -> repositories.JourneyRepository:
        return repositories.JourneyRepository()


class StopJourneyAPIView(generics.UpdateAPIView):
    serializer_class = serializers.JourneyStopSerializer

    def perform_update(self, serializer) -> None:
        repo = self.get_repository()
        notifier = notifiers.Notifier()
        journey = self.get_object()
        usecase = usecases.StopJourney(repo, notifier).set_params(
            serializer.validated_data
        )
        usecase.execute(journey)
       
    def get_object(self):
        repo = self.get_repository()
        id = self.kwargs.get('id')
        try:
            return repo.get_journey(id=id)
        except ObjectDoesNotExist:
            raise Http404("No matche with Journey")

    def get_repository(self) -> repositories.JourneyRepository:
        return repositories.JourneyRepository()
