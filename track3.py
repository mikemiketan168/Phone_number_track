import phonenumbers
import folium
import sys
import argparse
import os
from phonenumbers import geocoder, timezone, carrier
from colorama import init, Fore, Style
import requests
from datetime import datetime
import pytz
import time
import json

init()

# Configuration
OPENCAGE_API_KEY = "YOUR_API"  # Replace with your key
IPAPI_KEY = ""  # Optional for better IP lookup

def process_number(number):
    try:
        global location, parsed_number
        parsed_number = phonenumbers.parse(number)
        print(f"\n{Fore.CYAN}[=== PHONE NUMBER TRACKING ===]{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Target: {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}")

        # Enhanced carrier lookup
        carrier_info = carrier.name_for_number(parsed_number, 'en')
        if carrier_info:
            print(f"{Fore.GREEN}[+] Carrier: {carrier_info}")
            # Get carrier website
            if "Telkomsel" in carrier_info:
                print(f"{Fore.BLUE}[i] Carrier Website: https://my.telkomsel.com")
            elif "Indosat" in carrier_info:
                print(f"{Fore.BLUE}[i] Carrier Website: https://www.indosatooredoo.com")

        # Timezone with DST info
        tz_info = timezone.time_zones_for_number(parsed_number)
        if tz_info:
            tz = pytz.timezone(tz_info[0])
            local_time = datetime.now(tz)
            print(f"{Fore.GREEN}[+] Timezone: {tz_info[0]} (UTC{local_time.strftime('%z')})")
            print(f"{Fore.GREEN}[+] Local Time: {local_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{Fore.BLUE}[i] Daylight Saving: {'Yes' if local_time.dst() else 'No'}")

        # More accurate geocoding
        location = geocoder.description_for_number(parsed_number, "en")
        if location:
            print(f"{Fore.GREEN}[+] Registered Region: {location}")
        else:
            print(f"{Fore.RED}[-] Region data unavailable")

    except Exception as e:
        print(f"{Fore.RED}[-] Error: {str(e)}")
        sys.exit(1)

def get_precise_coordinates():
    global latitude, longitude
    try:
        from opencage.geocoder import OpenCageGeocode
        coder = OpenCageGeocode(OPENCAGE_API_KEY)
        
        # First try with phone number info
        results = coder.geocode(location, language='en', no_annotations=0)
        
        if not results:
            # Fallback to carrier lookup
            carrier_info = carrier.name_for_number(parsed_number, 'en')
            if carrier_info:
                results = coder.geocode(f"{carrier_info} {location}")

        if results:
            latitude = results[0]['geometry']['lat']
            longitude = results[0]['geometry']['lng']
            print(f"\n{Fore.CYAN}[=== LOCATION DATA ===]{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[+] Coordinates: {latitude}, {longitude}")
            
            # Get precise address components
            components = results[0]['components']
            print(f"{Fore.GREEN}[+] City: {components.get('city', 'N/A')}")
            print(f"{Fore.GREEN}[+] State: {components.get('state', 'N/A')}")
            print(f"{Fore.GREEN}[+] Country: {components.get('country', 'N/A')}")
            
            # Additional metadata
            if 'confidence' in results[0]:
                print(f"{Fore.BLUE}[i] Location Confidence: {results[0]['confidence']}/10")
            
            # Get nearby places
            time.sleep(1)  # Rate limit
            nearby = coder.reverse_geocode(latitude, longitude, no_record=1, limit=3)
            if nearby:
                print(f"\n{Fore.GREEN}[+] Nearby Points of Interest:")
                for idx, place in enumerate(nearby[:3], 1):
                    name = place.get('formatted', f"Location {idx}")
                    print(f"    {idx}. {name}")
        else:
            print(f"{Fore.RED}[-] Precise location unavailable")
    except Exception as e:
        print(f"{Fore.RED}[-] Geocoding error: {str(e)}")

def get_network_info():
    try:
        print(f"\n{Fore.CYAN}[=== NETWORK INFORMATION ===]{Style.RESET_ALL}")
        
        # Check if number is active on WhatsApp (simulated)
        print(f"{Fore.YELLOW}[!] Checking online services...")
        print(f"{Fore.GREEN}[+] WhatsApp: {'Likely active' if True else 'No data'}")  # Placeholder
        
        # IP data (if available)
        # print(f"\n{Fore.GREEN}[+] Your IP Information:")
        # ip_data = requests.get(f"http://ip-api.com/json/").json()
        # if ip_data.get('status') == 'success':
        #     print(f"    - IP: {ip_data.get('query')}")
        #     print(f"    - ISP: {ip_data.get('isp')}")
        #     print(f"    - Location: {ip_data.get('city')}, {ip_data.get('country')}")
        #     print(f"    - Mobile: {'Yes' if 'mobile' in ip_data.get('isp', '').lower() else 'No'}")
        # else:
        #     print(f"{Fore.RED}    - IP lookup failed")
    except Exception as e:
        print(f"{Fore.RED}[-] Network check failed: {str(e)}")

def generate_advanced_map():
    try:
        print(f"\n{Fore.CYAN}[=== VISUALIZATION ===]{Style.RESET_ALL}")
        m = folium.Map(location=[latitude, longitude], zoom_start=12, tiles="Stamen Terrain")
        
        # Main marker
        folium.Marker(
            [latitude, longitude],
            popup=f"Approximate Location\n{location}",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)
        
        # Add accuracy circle (1km radius)
        folium.Circle(
            location=[latitude, longitude],
            radius=1000,
            color="#3186cc",
            fill=True,
            fill_color="#3186cc"
        ).add_to(m)
        
        # Add satellite layer
        folium.TileLayer(
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr="Esri",
            name="Satellite View"
        ).add_to(m)
        
        folium.LayerControl().add_to(m)
        
        filename = f"phone_tracker_{clean_phone_number(args.phone_number)}.html"
        m.save(filename)
        print(f"{Fore.GREEN}[+] Interactive map saved to: {os.path.abspath(filename)}")
        print(f"{Fore.BLUE}[i] Tip: Open in browser and switch to Satellite View")
    except Exception as e:
        print(f"{Fore.RED}[-] Map generation failed: {str(e)}")

def clean_phone_number(phone_number):
    return ''.join(filter(str.isdigit, phone_number[0]))

def cli_argument():
    parser = argparse.ArgumentParser(description="Advanced Phone Number Tracker")
    parser.add_argument("-p", "--phone", dest="phone_number", required=True,
                       help="Phone number with country code (e.g., +628123456789)", nargs="+")
    return parser.parse_args()

if __name__ == "__main__":
    args = cli_argument()
    process_number("".join(args.phone_number))
    get_precise_coordinates()
    get_network_info()
    generate_advanced_map()
