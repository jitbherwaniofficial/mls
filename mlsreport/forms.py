from django import forms
from django.forms import inlineformset_factory
from mlsreport.models import MLSReport, Room

class MLSReportForm(forms.ModelForm):
    class Meta:
        model = MLSReport
        fields = [
            'property_image', 'property_address', 'tag', 'postal_code_address',
            'taxes', 'taxes_year', 'lot_plan', 'spis', 'no_of_rooms', 'bedrooms',
            'washrooms', 'parkings', 'detached', 'link', 'front_on', 'acre', 
            'dir_cross_st', 'irreg', 'client_desc', 'extras', 'mls_number', 
            'holdover', 'pin_number', 'possession_remarks', 'arn_number', 
            'occupancy', 'contact_after_expiry', 'basic_needs', 'kitchens', 
            'family_room', 'basement', 'fireplace_stv', 'heat', 'air_conditioning', 
            'central_vac', 'approximate_age', 'approximate_sqft', 'assesment', 
            'potl', 'elevator_lift', 'laundry_lev', 'physical_hdcp_eqp', 'exterior', 
            'drive', 'garage_parking_space', 'total_parkings', 'uffi', 'pool', 
            'energy_certificate', 'certificate_level', 'green_pis', 'prop_feat'
        ]


# Inline formset for Room model
RoomFormSet = inlineformset_factory(
    MLSReport,  # Parent model
    Room,       # Child model
    fields=["room_title", "room_level", "room_length", "room_width", "room_description"],
    extra=1,    # Number of empty forms to display
    can_delete=True  # Allow forms to be removed
)
