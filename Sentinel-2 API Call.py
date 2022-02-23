from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date

api = SentinelAPI('yourUsername', 'yourPassword', 'https://apihub.copernicus.eu/apihub')

# search by polygon, time, and Hub query keywords
footprint = geojson_to_wkt(read_geojson(r"GtheGeojsonFilePathOfYourStudyArea.geojson"))
products = api.query(footprint,
                     date = ('fromDate', 'toDate'), #from and to dates in 'yyyymmdd' format
                     platformname = 'Sentinel-2',
                     cloudcoverpercentage = (0, 30)) #range of cloudcoverage

productID = list(products) #creating a list of product IDs
print('Total no of data : ', len(productID))

monthList = [1,2,3,4,5,6,7,8,9,10,11,12]
monthWiseProduct = {}

for product in productID:
    month = int(products[product]['beginposition'].strftime("%m"))
    #extracting the month from the OrderedDict
    
    monthWiseProduct.setdefault(month, list()).append(product) 
    #creating a dictionary with month as key and list of productIDs as values

# Downloading one imagery per month which has the least cloudcoverage

cloudList = {}

for month, productsList in monthWiseProduct.items():
    print('Month : ', month)
    for product in productsList:
        cloud = float(products[product]['cloudcoverpercentage'])
        #extracting the cloud cover % value from the OrderedDict

        cloudList[cloud] = product
    print(cloudList,'\n')
    while(True):
        try:
            print('Product ID :', cloudList[min(cloudList)])
            api.download(cloudList[min(cloudList)],'OutputDirectory')
            #download the imagery having least cloud coverage %
            break
        except:
            #if anything went wrong while trying to download, selecting the next least one
            print("An error occurred while downloading the product '{}' \nTrying the next one...".format(cloudList[min(cloudList)]))
            del cloudList[min(cloudList)]       
    cloudList = {} #reinitialising the dictionary for the next month