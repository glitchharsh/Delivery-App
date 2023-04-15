from django.urls import path
from .views import TransportRequestView, RiderTravelInfoView, MyRequestsView, MatchedRequestView, ApplyForRiderView

urlpatterns = [
    path('request/', TransportRequestView.as_view(), name='request_transport'),
    path('upload/', RiderTravelInfoView.as_view(), name='upload_ride'),
    path('request/view/', MyRequestsView.as_view(), name='view_requests'),
    path('matched/<int:id>/', MatchedRequestView.as_view(), name='matched_rides'),
    path('matched/<int:id_request>/apply/<int:id_ride>/', ApplyForRiderView.as_view(), name='apply_for_ride')
]