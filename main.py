from bs4 import BeautifulSoup
import csv
import urllib3.request

csvPages = 'pages.csv'
csvLocation = 'altTextFails.csv'
tempFileLocation = 'tempFile.html'

with open(csvPages, newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    # Open CSV and write links to the CSV File
    with open(csvLocation, mode='w') as csvFile:
        fieldnames = ['page_title', 'page_address', 'image' ]
        csv_writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        csv_writer.writeheader()

        for row in reader:
            webpage = row['pages']
            try:

                http = urllib3.PoolManager()

                response = http.request('GET', webpage)
                soup = BeautifulSoup(response.data, "html.parser")

                rawTitle = soup.title.string
                rawTitleSplit = rawTitle.split(" |")
                pageTitle = '"' + rawTitleSplit[0] + '"'

                # Select all the images
                images = soup.findAll('img', alt=False)

                for image in images:
                    # for iframe
                    csv_writer.writerow({'page_title': pageTitle,'page_address': webpage,'image': image})

                # Output final count for manual verification
                print("Written to CSV. There are " + str(len(images)) + " images found!")


            except:
                print("Oops! Error!")
