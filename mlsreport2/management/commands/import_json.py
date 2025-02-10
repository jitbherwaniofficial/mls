import json
import os
from django.core.management.base import BaseCommand
from mlsreport2.models import Realtor, Property, ListingInfo, PropertyInfo, Room, Washroom
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Import JSON data into PostgreSQL and clear the file after importing"

    def handle(self, *args, **kwargs):
        json_file_path = r"E:\jit\python\django\mls\mls.json"

        if not os.path.exists(json_file_path) or os.stat(json_file_path).st_size == 0:
            self.stdout.write(self.style.WARNING("JSON file is empty or missing. Nothing to import."))
            return

        with open(json_file_path, "r") as file:
            try:
                data = json.load(file)
                if not data:
                    self.stdout.write(self.style.WARNING("JSON file is empty. No data to import."))
                    return
            except json.JSONDecodeError:
                self.stdout.write(self.style.ERROR("Invalid JSON format. Skipping import."))
                return

        # Import Data
        self.import_json_data(data)

        # Clear JSON File After Successful Import
        with open(json_file_path, "w") as file:
            file.write("[]")  # Overwrite with empty JSON array

        self.stdout.write(self.style.SUCCESS("Successfully imported JSON data and cleared the JSON file"))

    def import_json_data(self, data):
        """
        Processes JSON data and saves it into the database.
        """
        for entry in data:
            # Fix Realtor get_or_create
            realtor, _ = Realtor.objects.get_or_create(
                name=entry["realtor"],
                defaults={"designation": entry["designation"]}
            )

            # Fix features JSON decoding
            try:
                features = json.loads(entry["features_1"].replace("'", "\""))
            except json.JSONDecodeError:
                features = {}

            # Ensure main_image is not too long
            main_image = entry["main_image"][:1500]

            default_user = User.objects.first()
            if not default_user:
                default_user = User.objects.create(username="defaultuser")

            property_obj = Property.objects.create(
                user=default_user,
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
                main_image=main_image,
                client_remark=entry["client_remark"],
                extras=entry.get("extras", ""),
            )

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

            # Check for missing "Room" data
            if "Room" in entry["tables"]:
                for idx, room_name in enumerate(entry["tables"]["Room"].get("Room", [])):
                    Room.objects.create(
                        property=property_obj,
                        name=room_name,
                        level=entry["tables"]["Room"]["Level"][idx],
                        dimensions=entry["tables"]["Room"]["Dimensions"][idx],
                        notes=entry["tables"]["Room"]["Notes"][idx],
                    )

            # Check for missing "Washrooms" data
            if "# of Washrooms" in entry["tables"]:
                for idx, pieces in enumerate(entry["tables"]["# of Washrooms"].get("Pieces", [])):
                    Washroom.objects.create(
                        property=property_obj,
                        pieces=int(pieces),
                        level=entry["tables"]["# of Washrooms"]["Level"][idx],
                    )
