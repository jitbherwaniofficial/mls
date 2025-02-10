from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render, get_object_or_404
from .models import MLSReport
from .forms import MLSReportForm, RoomFormSet
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.templatetags.static import static
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def create_mls_report(request):
    if request.method == 'POST':
        # Bind the main MLSReport form and inline RoomFormSet
        mls_form = MLSReportForm(request.POST, request.FILES)
        if mls_form.is_valid():
            mls_report = mls_form.save(commit=False)  # Save without committing to the DB
            mls_report.user = request.user  # Assign the current user if applicable
            mls_report.save()  # Now save to the DB

            # Bind RoomFormSet to the saved MLSReport instance
            room_formset = RoomFormSet(request.POST, instance=mls_report)
            if room_formset.is_valid():
                room_formset.save()
                # Redirect to the newly created MLSReport view
                return redirect('view_mls_report', pk=mls_report.pk)
        else:
            room_formset = RoomFormSet(request.POST)
    else:
        # Render empty forms for both MLSReport and RoomFormSet
        mls_form = MLSReportForm()
        room_formset = RoomFormSet()

    return render(request, 'create_mls_report.html', {
        'mls_form': mls_form,
        'room_formset': room_formset,
    })


@login_required
def edit_mls_report(request, pk):
    # Fetch the existing MLSReport instance
    mls_report = get_object_or_404(MLSReport, pk=pk)

    if request.method == 'POST':
        # Bind the form with the POST data and the existing MLSReport instance
        mls_form = MLSReportForm(request.POST, request.FILES, instance=mls_report)
        room_formset = RoomFormSet(request.POST, instance=mls_report)

        if mls_form.is_valid() and room_formset.is_valid():
            # Save the updated MLSReport
            mls_form.save()

            # Save the inline RoomFormSet
            room_formset.save()

            # Redirect to the view of the updated MLSReport
            return redirect('home') #, pk=mls_report.pk
        
    else:
        # Pre-fill the form with the existing MLSReport data
        mls_form = MLSReportForm(instance=mls_report)
        room_formset = RoomFormSet(instance=mls_report)

    return render(request, 'edit_mls_report.html', {
        'mls_form': mls_form,
        'room_formset': room_formset
    })




def view_mls_report(request, pk):
    # Fetch the MLSReport and related rooms
    report = get_object_or_404(MLSReport, pk=pk)
    rooms = report.rooms.all()  # Related Room instances

    return render(request, 'view_mls_report.html', {
        'report': report,
        'rooms': rooms,
    })



def generate_mls_report(request, pk):
    try:
        report = MLSReport.objects.get(pk=pk)
        rooms = report.rooms.all()  # Related Room instances
        property_image_url = request.build_absolute_uri(report.property_image.url)
        basic_needs = report.basic_needs.all()

        icons = []

        # Loop through basic_needs and check if the icon is not None
        for basic in basic_needs:
            if basic.icon:
                icon_url = request.build_absolute_uri(basic.icon.url)
            else:
                icon_url = None  # Or provide a default icon URL
            icons.append(icon_url)

        # Combine basic_needs and icons into a list of tuples
        basic_needs_with_icons = zip(basic_needs, icons)


    except MLSReport.DoesNotExist:
        raise Http404("MLS Report not found")
    
    context = {
        'report': report,
        'property_image_url' : property_image_url,
        'basic_needs':basic_needs,
        'basic_needs_with_icons': basic_needs_with_icons,  # Pass the combined list
        'rooms':rooms
    }

    css_file = CSS(request.build_absolute_uri(static('css/mlsreport.css')))
    # Render the HTML using a template and context
    html_string = render_to_string('view_mls_report.html', context)

    # Generate the PDF from the rendered HTML
    # pdf = HTML(string=html_string).write_pdf()
    pdf = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf(stylesheets=[css_file])

    # Return the PDF as a response
    return HttpResponse(pdf, content_type="application/pdf")

 