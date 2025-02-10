from django import forms
from django.forms import inlineformset_factory
from .models import Property, ListingInfo, PropertyInfo, Room, Washroom

# ✅ Main Property Form
class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'realtor',
            'address_1',
            'address_2',
            'address_3',
            'address_4',
            'title',
            'condition',
            'status',
            'price',
            'taxes',
            'features',
            'main_image',
            'client_remark',
            'extras',
        ]
        widgets = {
            'features': forms.Textarea(attrs={'rows': 3}),
        }

# ✅ Forms for ListingInfo & PropertyInfo
class ListingInfoForm(forms.ModelForm):
    class Meta:
        model = ListingInfo
        fields = "__all__"

class PropertyInfoForm(forms.ModelForm):
    class Meta:
        model = PropertyInfo
        fields = "__all__"

# ✅ Forms for Room & Washroom (Many-to-One Relations)
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Room Name'}),
            'dimensions': forms.TextInput(attrs={'placeholder': 'e.g., 10x12 ft'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Additional Notes'}),
        }

class WashroomForm(forms.ModelForm):
    class Meta:
        model = Washroom
        fields = "__all__"

# ✅ Optimized Inline Formsets
RoomFormSet = inlineformset_factory(
    Property, Room, form=RoomForm, extra=2, can_delete=True
)

WashroomFormSet = inlineformset_factory(
    Property, Washroom, form=WashroomForm, extra=2, can_delete=True
)

class JSONUploadForm(forms.Form):
    json_file = forms.FileField(label="Upload JSON File")