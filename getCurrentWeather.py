import requests
import xml.etree.ElementTree as ET


def getCurrentWeather(city,output_format):
    base_url = "https://weatherapi-com.p.rapidapi.com/current.json"
    headers = {
	"X-RapidAPI-Key": " ",
	"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }
    params = {
        "q": city
    }
    try:
        response = requests.get(base_url,headers=headers, params=params)
        weather_data = {}
        if response.status_code == 200:
            data = response.json()
            if data and data.get('location') and data.get('current'):
                lat = data.get('location').get('lat')
                lon = data.get('location').get('lon')
                city = data.get('location').get('name')
                temp = str(data.get('current').get('temp_c'))+' C'
                weather_data["Weather"] = temp
                weather_data["Latitude"] = lat
                weather_data["Longitude"] = lon
                weather_data["City"] = city
                if output_format == "XML":
                    root_element = parse_element('root', weather_data)
                    xml_data = ET.tostring(root_element, encoding='unicode')
                    return xml_data
                else:
                    return weather_data
        else:
            return "Failed to retrieve weather data.", 500
    except:
        return "Requested data not getting"
    
def parse_element(key, value):
    """"Convert JSON into XML format"""
    element = ET.Element(key)
    if isinstance(value, dict):
        for child_key, child_value in value.items():
            child_element = parse_element(child_key, child_value)
            element.append(child_element)
    else:
        element.text = str(value)
    return element

