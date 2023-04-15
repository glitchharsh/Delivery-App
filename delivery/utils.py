from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from .models import TransportRequest, RiderTravelInfo

def get_matching_rides(request_id):
    # utility function to return matching rides for a request
    try:
        request = TransportRequest.objects.get(pk=request_id)
        if request_id:
            queryset = RiderTravelInfo.objects.filter(
                source=request.source,
                destination=request.destination,
                date_and_time__date=request.date_and_time.date(),
                )
        if not request.flexible_timings:
            queryset = queryset.filter(
                date_and_time__lte=request.date_and_time,
                date_and_time__gte=request.date_and_time - timedelta(hours=2))
        return queryset
    except ObjectDoesNotExist:
        return None