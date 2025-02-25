from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


htmlLoc = r'D:\Documentos\SPJain\Term2\Intro\Project\html\\'

dataDict = {'Link': [],
            "Price": [],
            "Bedrooms": [],
            "Bathrooms": [],
            "Parking": [],
            "Size": [],
            "Measure": [],
            "Location": [],
            "Type": []}

detailsSprites = {
    'Bathrooms': '#ck-sprite-baths',
    'Bedrooms': '#ck-sprite-beds',
    'Parking': '#ck-sprite-cars'
}

# Until 301 main suburbs of Sydney
amountHTML = 1063

# For just sydney from page number 81
for numberHTML in range(81, amountHTML+1):
    # Read the HTML file
    with open(htmlLoc + 'page' + str(numberHTML) + '.txt', 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all <li> elements
    list_items = soup.find_all('li')

    # Iterate through each <li> element and check for the presence of the target class
    for index, li in enumerate(list_items):
        try:
            link_element = li.find('a', class_='details-link residential-card__details-link')
            if link_element:
                link = link_element.get('href')
                if link in dataDict['Link']:
                    raise Exception('This property has being already extracted.')
                else:
                    dataDict['Link'].append(link)
            else:
                raise Exception('This property has no identifier.')
            # Search elements in the container
            property_details = li.find('div', class_='residential-card__content')
            if property_details:
                for name in detailsSprites:
                    # Check if the detail div contains a specific icon
                    if property_details.find('use', href=detailsSprites[name]):
                        dataDict[name].append(property_details.find('p', class_='Text__Typography-sc-vzn7fr-0').get_text())
                    else:
                        dataDict[name].append(np.nan)

                class_size = 'View__PropertySizeGroup-sc-1psmy31-1 khUTtT property-size-group'
                property_size_div = property_details.find('div', class_=class_size)

                # Extract the text after the svg element
                if property_size_div:
                    # Get all text content from the div, including non-breaking spaces
                    text_content = property_size_div.get_text(strip=True)

                    # Split the text content to find the numerical value
                    text_parts = text_content.split()

                    # Assuming the numerical value is the last part of the text
                    if text_parts:
                        property_size = text_parts[-1]
                        dataDict['Size'].append(property_size)

                        # Get measure of the size
                        measure_class = 'View__PropertySize-sc-1psmy31-0 fcddko property-size'
                        property_measure_div = property_details.find('div', class_=measure_class)
                        if property_measure_div:
                            measure_text = property_measure_div.find('span').get_text(strip=True)
                            dataDict['Measure'].append(measure_text)
                        else:
                            dataDict['Measure'].append(np.nan)
                    else:
                        dataDict['Size'].append(np.nan)

                else:
                    dataDict['Size'].append(np.nan)
                    dataDict['Measure'].append(np.nan)

                # Check property type
                property_type = li.find('span', class_={'residential-card__property-type'})
                if property_type:
                    dataDict['Type'].append(property_type.get_text())
                else:
                    dataDict['Type'].append(np.nan)

                # Get Suburb
                details_link = soup.find('a', class_='details-link residential-card__details-link')

                if details_link:
                    # Extract the text from the span element within the 'a' element
                    span_text = details_link.find('span').get_text()

                    # Split the text by comma and get the part after the comma
                    parts = span_text.split(',')
                    if len(parts) > 1:
                        location = parts[1].strip()
                        dataDict['Location'].append(location)

                    else:
                        dataDict['Location'].append(np.nan)

                else:
                    dataDict['Location'].append(np.nan)
            # Add nan values
            else:
                for name in detailsSprites:
                    dataDict[name].append(np.nan)
                dataDict['Size'].append(np.nan)
                dataDict['Type'].append(np.nan)
                dataDict['Location'].append(np.nan)
                dataDict['Measure'].append(np.nan)

            # Check if there is any element inside <li> with the target class
            target_element = li.find(class_='property-price')
            if target_element:
                dataDict["Price"].append(target_element.text)
            else:
                dataDict["Price"].append(np.nan)
            print(f'Data extracted from page {numberHTML}')
        except:
            print(f'No data to extract in page {numberHTML}')
            pass

print(dataDict)
for i in dataDict:
    print(i)
    print(len(dataDict[i]))

df = pd.DataFrame.from_dict(dataDict)

df.to_csv('data.csv')
