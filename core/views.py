from django.shortcuts import render
# from mlsreport.models import MLSReport
from mlsreport2.models import Property, ListingInfo, PropertyInfo, Room, Washroom
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def home(request):
    # mls_report = MLSReport.objects.filter(user=request.user)
    properties = Property.objects.filter(user=request.user)
    context = {
        # 'mls_report': mls_report,
        'properties':properties
        }
    return render(request, 'home.html', context)
