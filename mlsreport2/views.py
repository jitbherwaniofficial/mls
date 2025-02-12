from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory

from mls import settings
from .models import Property, ListingInfo, PropertyInfo, Room, Washroom
from .forms import PropertyForm, ListingInfoForm, PropertyInfoForm, RoomFormSet, WashroomFormSet
from django.contrib.auth.decorators import login_required

import json
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Property, Realtor, ListingInfo, PropertyInfo, Room, Washroom
from .forms import PropertyForm, ListingInfoForm, PropertyInfoForm, RoomFormSet, WashroomFormSet, JSONUploadForm

@login_required
def create_property(request):
    """
    Handles JSON file upload and manual MLS property creation separately.
    """
    json_form = JSONUploadForm()
    property_form = PropertyForm()
    listing_info_form = ListingInfoForm()
    property_info_form = PropertyInfoForm()
    room_formset = RoomFormSet()
    washroom_formset = WashroomFormSet()

    if request.method == "POST":
        # 🔹 Check if JSON Upload Button was Clicked
        if "json_upload" in request.POST:
            json_form = JSONUploadForm(request.POST, request.FILES)
            if json_form.is_valid():
                json_file = request.FILES["json_file"]  # Use correct field name
                try:
                    data = json.load(json_file)

                    for entry in data:
                        # Handle Realtor
                        realtor, _ = Realtor.objects.get_or_create(
                            name=entry["realtor"],
                            defaults={"designation": entry["designation"]}
                        )

                        # Ensure features is stored as a valid JSON dictionary
                        features = entry.get("features_1", {})

                        # Convert string JSON to dictionary if necessary
                        if isinstance(features, str):
                            try:
                                features = json.loads(entry["features_1"].replace("'", "\""))
                            except json.JSONDecodeError:
                                features = {}  # Default to empty dictionary if invalid

                        # Create Property
                        property_obj = Property.objects.create(
                            user=request.user,  # ✅ Assign the logged-in user
                            realtor=realtor,
                            address_1=entry["address_1"],
                            address_2=entry.get("address_2", ""),
                            address_3=entry.get("address_3", ""),
                            address_4=entry.get("address_4", ""),
                            title=entry["title"],
                            condition=entry["condition"],
                            status=entry["status"],
                            price=entry["price"],
                            taxes=entry["taxes"],
                            features=features,
                            main_image=entry["main_image"][:1500],
                            client_remark=entry["client_remark"],
                            extras=entry.get("extras", ""),
                        )

                        # Create ListingInfo
                        ListingInfo.objects.create(
                            property=property_obj,
                            pin_number=entry["listing_info"]["PIN#"],
                            taxes=entry["listing_info"]["Taxes"],
                            tax_year=entry["listing_info"]["Tax Year"],
                            legal_description=entry["listing_info"]["Legal Description"],
                            status=entry["listing_info"]["Status"],
                            possession_remarks=entry["listing_info"].get("Possession Remarks", ""),
                            seller_info=entry["listing_info"]["Seller Property Info Statement"],
                        )

                        # Create PropertyInfo
                        PropertyInfo.objects.create(
                            property=property_obj,
                            approx_age=entry["property_info"]["Approx Age"],
                            fronting_on=entry["property_info"]["Fronting On"],
                            lot_size=entry["property_info"]["Lot Size"],
                            square_feet=entry["property_info"]["Square Feet"],
                            drive=entry["property_info"]["Drive"],
                            total_parking_spaces=int(entry["property_info"]["Total Parking Spaces"]),
                            pool=entry["property_info"].get("Pool", ""),
                            air_conditioning=entry["property_info"]["A/C"],
                            heating_source=entry["property_info"]["heating Source"],
                            heating_type=entry["property_info"]["heating Type"],
                            water=entry["property_info"]["Water"],
                            sewers=entry["property_info"]["Sewers"],
                        )

                        # Create Rooms
                        if "Room" in entry["tables"]:
                            for idx, room_name in enumerate(entry["tables"]["Room"].get("Room", [])):
                                Room.objects.create(
                                    property=property_obj,
                                    name=room_name,
                                    level=entry["tables"]["Room"]["Level"][idx],
                                    dimensions=entry["tables"]["Room"]["Dimensions"][idx],
                                    notes=entry["tables"]["Room"]["Notes"][idx],
                                )

                        # Create Washrooms
                        if "# of Washrooms" in entry["tables"]:
                            for idx, pieces in enumerate(entry["tables"]["# of Washrooms"].get("Pieces", [])):
                                Washroom.objects.create(
                                    property=property_obj,
                                    pieces=int(pieces),
                                    level=entry["tables"]["# of Washrooms"]["Level"][idx],
                                )

                    messages.success(request, "JSON data successfully imported!")
                    return redirect("home")  # Refresh the form

                except json.JSONDecodeError:
                    messages.error(request, "Invalid JSON file. Please upload a valid file.")

            return redirect("home")  # Prevents manual form validation

        # 🔹 Process manual form submission separately
        property_form = PropertyForm(request.POST)
        listing_info_form = ListingInfoForm(request.POST)
        property_info_form = PropertyInfoForm(request.POST)
        room_formset = RoomFormSet(request.POST)
        washroom_formset = WashroomFormSet(request.POST)

        if all([
            property_form.is_valid(),
            listing_info_form.is_valid(),
            property_info_form.is_valid(),
            room_formset.is_valid(),
            washroom_formset.is_valid(),
        ]):
            property_obj = property_form.save()
            listing_info = listing_info_form.save(commit=False)
            listing_info.property = property_obj
            listing_info.save()

            property_info = property_info_form.save(commit=False)
            property_info.property = property_obj
            property_info.save()

            room_formset.instance = property_obj
            room_formset.save()

            washroom_formset.instance = property_obj
            washroom_formset.save()

            return redirect("home", pk=property_obj.pk)

    context = {
        "property_form": property_form,
        "listing_info_form": listing_info_form,
        "property_info_form": property_info_form,
        "room_formset": room_formset,
        "washroom_formset": washroom_formset,
        "json_form": json_form,
    }
    return render(request, "create_property.html", context)




@login_required
def view_property_mls(request, pk):
    """
    Display the details of a specific property, including related ListingInfo, 
    PropertyInfo, Rooms, and Washrooms.
    """
    property_obj = get_object_or_404(Property, pk=pk)

    context = {
        "property": property_obj,
        "listing_info": property_obj.listing_info,   
        "property_info": property_obj.property_info, 
        "rooms": property_obj.rooms.all(),         
        "washrooms": property_obj.washrooms.all(), 
    }
    
    return render(request, "view_property_mls.html", context)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Property, ListingInfo, PropertyInfo
from .forms import PropertyForm, ListingInfoForm, PropertyInfoForm, RoomFormSet, WashroomFormSet

@login_required
def update_property(request, pk):
    """
    Allows a user to update a property along with ListingInfo, PropertyInfo,
    and inline Room & Washroom formsets.
    """
    property_obj = get_object_or_404(Property, pk=pk)
    listing_info, _ = ListingInfo.objects.get_or_create(property=property_obj)
    property_info, _ = PropertyInfo.objects.get_or_create(property=property_obj)

    if request.method == "POST":
        property_form = PropertyForm(request.POST, instance=property_obj)
        listing_info_form = ListingInfoForm(request.POST, instance=listing_info)
        property_info_form = PropertyInfoForm(request.POST, instance=property_info)
        room_formset = RoomFormSet(request.POST, instance=property_obj)
        washroom_formset = WashroomFormSet(request.POST, instance=property_obj)

        if (
            property_form.is_valid() and
            listing_info_form.is_valid() and
            property_info_form.is_valid() and
            room_formset.is_valid() and
            washroom_formset.is_valid()
        ):
            property_form.save()
            listing_info_form.save()
            property_info_form.save()
            room_formset.save()
            washroom_formset.save()
            
            return redirect("home") #, pk=property_obj.pk  

    else:
        property_form = PropertyForm(instance=property_obj)
        listing_info_form = ListingInfoForm(instance=listing_info)
        property_info_form = PropertyInfoForm(instance=property_info)
        room_formset = RoomFormSet(instance=property_obj)
        washroom_formset = WashroomFormSet(instance=property_obj)

    context = {
        "property_form": property_form,
        "listing_info_form": listing_info_form,
        "property_info_form": property_info_form,
        "room_formset": room_formset,
        "washroom_formset": washroom_formset,
        "property": property_obj,
    }
    return render(request, "update_property.html", context)


from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseServerError
from weasyprint import HTML, CSS
from django.template.loader import render_to_string
from .models import Property
import logging
from django.templatetags.static import static

# Set up logging
logger = logging.getLogger(__name__)

from weasyprint import default_url_fetcher
import ssl

def custom_url_fetcher(url, timeout=120, **kwargs):
    # Bypass SSL verification for Railway's HTTPS
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    return default_url_fetcher(
        url,
        ssl_context=ssl_context,
        timeout=timeout
    )


def generate_mls_pdf(request, pk):
    """
    Generates a PDF for the property detail (MLS) page with error handling.
    """
    try:
        # Fetch property or return 404 if not found
        property_obj = get_object_or_404(Property, pk=pk)

        # Fetch related models
        listing_info = ListingInfo.objects.filter(property=property_obj).first()
        property_info = PropertyInfo.objects.filter(property=property_obj).first()
        rooms = Room.objects.filter(property=property_obj)
        washrooms = Washroom.objects.filter(property=property_obj)

        for room in rooms:
            if isinstance(room.dimensions, list) and len(room.dimensions) > 1:
                # Extract the feet dimension from the second list item
                ft_dimension = room.dimensions[1][0]  # Get "(16.73 ft x 12.99 ft)"
                
                # Remove parentheses and split width & height
                ft_dimension = ft_dimension.replace("(", "").replace(")", "")  # "16.73 ft x 12.99 ft"
                width, height = ft_dimension.split(" x ")  # ["16.73 ft", "12.99 ft"]

                room.width_ft = width.strip()  # "16.73 ft"
                room.height_ft = height.strip()  # "12.99 ft"
            else:
                room.width_ft = "N/A"
                room.height_ft = "N/A"


        context = {
            "property": property_obj,
            "listing_info": listing_info,
            "property_info": property_info,
            "rooms": rooms,
            "washrooms": washrooms,
        }

                # Add static URL with absolute path to context
        context["static_base_url"] = request.build_absolute_uri(static(""))


        # Render the template with the property data
        html_string = render_to_string("view_property_mls.html", context)

        # css_file = CSS(request.build_absolute_uri(static('css/mlsreport.css')))
        # import os
        # css_path = os.path.join(settings.STATIC_ROOT, 'css/mlsreport.css')
        # css_file = CSS(filename=css_path)

        # Generate CSS with proper base URL
        css = CSS(
            string=render_to_string("css/mlsreport.css", context),
            base_url=request.build_absolute_uri("/")
        )

        # Generate PDF with proper base URL
        html = HTML(
            string=html_string,
            base_url=request.build_absolute_uri("/"),
            url_fetcher=custom_url_fetcher  # Add custom fetcher from previous solution
        )

        # Generate the PDF
        # pdf = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf(stylesheets=[css_file], timeout=120)
        # pdf = HTML(string=html_string).write_pdf(stylesheets=[css_file], timeout=120)

        pdf = html.write_pdf(stylesheets=[css])

        # Return PDF response
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f'filename="MLS_{property_obj.pk}.pdf"'
        return response

    except Exception as e:
        logger.error(f"Error generating PDF for property {pk}: {e}")
        print(f"Error generating PDF for property {pk}: {e}")
        return HttpResponseServerError("An error occurred while generating the PDF. Please try again later.")
