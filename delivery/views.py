import pytz
from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from .serializers import TransportRequestSerializer, RiderTravelInfoSerializer, RiderTravelInfoWriteSerializer
from .models import TransportRequest, RiderTravelInfo, MatchedAssets
from .utils import get_matching_rides

class TransportRequestView(LoginRequiredMixin, generics.CreateAPIView):
    # view to make a transport request

    queryset = TransportRequest.objects.all()
    serializer_class = TransportRequestSerializer
    permission_classes = [IsAuthenticated]

class RiderTravelInfoView(LoginRequiredMixin, generics.CreateAPIView):
    # view to upload a ride schedule

    queryset = RiderTravelInfo.objects.all()
    serializer_class = RiderTravelInfoWriteSerializer
    permission_classes = [IsAuthenticated]

class MyRequestsView(LoginRequiredMixin, generics.ListAPIView):
    # view to return all of a user's requests

    serializer_class = TransportRequestSerializer
    permission_classes = [IsAuthenticated]

    filterset_fields = ['asset_types', 'asset_senstivity']
    ordering_fields = ['date_and_time']

    def get_queryset(self):
        # checking whether the requests are expired and updating the status of the request

        user = self.request.user
        queryset = None
        if user is not None:
            queryset = TransportRequest.objects.filter(requested_by=user)
            now = datetime.now()
            now = pytz.utc.localize(now)
            for obj in queryset:
                if obj.date_and_time <= now:
                    obj.status = 'EXPIRED'
                    obj.save()
        return queryset

class MatchedRequestView(LoginRequiredMixin, generics.ListAPIView):
    # view to display all matching rides to a corresponding request

    queryset = RiderTravelInfo.objects.all()
    serializer_class = RiderTravelInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        request_id = self.kwargs.get('id')
        queryset = TransportRequest.objects.none()

        # making sure that the current request is made by the logged in user
        try:
            request = TransportRequest.objects.get(pk=request_id)
        except ObjectDoesNotExist:
            return queryset
        if request.requested_by != user:
            return queryset

        return get_matching_rides(request_id)
            
class ApplyForRiderView(LoginRequiredMixin, views.APIView):
    # view to apply for a particular ride

    permission_classes = [IsAuthenticated]

    def get(self, request, id_request, id_ride):
        user = self.request.user

        # making sure that the current request is made by the logged in user
        try:
            request = TransportRequest.objects.get(pk=id_request)
        except ObjectDoesNotExist:
            return Response({'Error': 'Request Not Found'}, status=HTTP_400_BAD_REQUEST)
        if request.requested_by != user:
            return Response({'Error': 'Request Not By User'}, status=HTTP_401_UNAUTHORIZED)
        
        # making sure that the current ride does indeed match with the given request
        rides = get_matching_rides(id_request)
        if not rides:
            return Response({'Error': 'Ride Not Found'}, status=HTTP_400_BAD_REQUEST)
        rides = rides.values_list('id', flat=True)
        if id_ride not in rides:
            return Response({'Error': 'Ride Not Found'}, status=HTTP_400_BAD_REQUEST)
        
        # saving the match
        ride = RiderTravelInfo.objects.get(pk=id_ride)
        obj = MatchedAssets.objects.create(request=request, rider=ride, applied=True)
        ride.status = 'APPLIED'
        if ride.no_of_assets > request.no_of_assets:
            ride.no_of_assets = ride.no_of_assets - request.no_of_assets
        else:
            ride.no_of_assets = 0
        ride.save()

        return Response({'Info': 'Successfully Applied'}, status=HTTP_200_OK)
        
        





