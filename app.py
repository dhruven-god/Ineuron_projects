from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)

@app.route('/', methods=['GET']) # TO display the route
@cross_origin()

def home():
    return render_template('index.html')

@app.route('/review',methods=['POST'])

def form():

    if request.method == 'POST':
        searchString = request.form['content'].replace(" ","") # Remove the spacing given in the search bar
        try:
            
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString      # Connect the string with flipkart as an url
            uClient = uReq(flipkart_url) # Request the webpage
            flipkartPage = uClient.read() # Read the data from the webpage
            uClient.close() # Close the connection with webserver
            flipkart_html = bs(flipkartPage, "html.parser") # Using Beautiful soup parsing webpage as html
            bigboxes = flipkart_html.findAll("div", {"class": "_2pi5LC col-12-12"}) # Search for the tag using inspect
            del bigboxes[0:3] # Deleting first 3 elements as they don't have relevant info.
            box = bigboxes[0] # Taking all the iterations
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href'] # Getting the product link from <a> tag
            prodRes = requests.get(productLink) # getting the product page from server
            #prodRes.encoding='utf-8' # Encoding should be utf-8
            prod_html = bs(prodRes.text, "html.parser") # Parsing the page as html
            #print(prod_html)
            commentboxes = prod_html.find_all('div', {'class': "_16PBlm"}) # Finding the review div class #_3nrCtb

            reviews = []
            for commentbox in commentboxes:
                try:
                    name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text # Extracting the name from the box

                except:
                    name = 'No Name'

                try:
                    #rating.encode(encoding='utf-8')
                    rating = commentbox.div.div.div.div.text # Extracting the rating from the box


                except:
                    rating = 'No Rating'

                try:
                    #commentHead.encode(encoding='utf-8')
                    commentHead = commentbox.div.div.div.p.text # Extracting the COMMENTHEAD from the box

                except:
                    commentHead = 'No Comment Heading'
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': 't-ZTKy'}) # Extracting the COMMENT from the box
                    #custComment.encode(encoding='utf-8')
                    custComment = comtag[0].div.text
                except Exception as e:
                    print("Exception while creating dictionary: ",e)

                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                            "Comment": custComment}
                reviews.append(mydict)
            return render_template('results.html', reviews=reviews[0:(len(reviews)-1)])

        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')

if __name__ == "__main__":
    #app.run(port=8000, debug=True)
	app.run(debug=True)