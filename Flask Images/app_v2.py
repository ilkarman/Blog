from flask import Flask, render_template, request, send_file, json
from io import BytesIO
from PIL import Image, ImageOps
import json
import base64
import urllib.parse
import mxnet as mx
import numpy as np
from collections import namedtuple

Batch = namedtuple('Batch', ['data'])
app = Flask(__name__)

# Load Labels
with open('synset.txt', 'r') as f:
    synsets = [l.rstrip() for l in f]
with open('synset_es.txt', 'r') as f:
    synset_es = [l.rstrip() for l in f]
with open('synset_tr.txt', 'r') as f:
    synset_tr = [l.rstrip() for l in f]
with open('synset_ru.txt', 'r') as f:
    synset_ru = [l.rstrip() for l in f]
with open('synset_it.txt', 'r') as f:
    synset_it = [l.rstrip() for l in f]

available_languages = {
	"languages": [
		{'name':'Spanish', 'icon':'es.png'},
		{'name':'Italian', 'icon':'it.png'},
		{'name':'Turkish', 'icon':'tr.png'},
		{'name':'Russian', 'icon':'ru.png'}
		]}

# Load model
model = mx.model.FeedForward.load('resnet-152', 0, ctx=mx.cpu())
 
@app.route("/")
def index():
    return render_template('layout.html')

@app.route("/languages", methods=['GET'])
def return_languages():
	print(available_languages)
	return json.dumps(available_languages)

@app.route("/uploader_ios", methods=['POST'])
def upload_file_ios():
	# Get image from upload and stream into PIL object
	print('Mobile Request')
	imagefile = request.files['imagefile']
	img = Image.open(BytesIO(imagefile.read())).convert('RGB')
	print("Opened image")
	print(img.size)

	# Run some processing and get back image and data
	_, ret_dta_en, ret_dta_es, ret_dta_tr, ret_dta_ru, ret_dta_it = run_some_function_using_image_as_input(img)
	classification = {
		'English': ret_dta_en,
		'Spanish': ret_dta_es,
		'Italian': ret_dta_it,
		'Turkish': ret_dta_tr,
		'Russian': ret_dta_ru
	}

	print("Image: %s classified as %s" % (imagefile.filename, classification))
	classification_out = json.dumps(classification)

	return classification_out

def run_some_function_using_image_as_input(img):

	# Load image
	img = ImageOps.fit(img, (224, 224), Image.ANTIALIAS)
	
	# Change shape
	img_np = np.swapaxes(img, 0, 2)
	img_np = np.swapaxes(img_np, 1, 2) 
	img_np = img_np[np.newaxis, :] 

	# Prediction
	res = model.predict(mx.nd.array(img_np), mx.cpu())
	prob = np.squeeze(res)

	# Category
	a = np.argsort(prob)[-1]    
	classification = " ".join(synsets[a].split(" ")[1:]).split(",")[0]

	return img, classification, synset_es[a], synset_tr[a], synset_ru[a], synset_it[a]

#############
# OLD Follows
#############

# For web-interface ... temporary
@app.route("/uploader", methods=['POST'])
def upload_file():
	# Get image from upload and stream into PIL object
	imagefile = request.files['imagefile']
	try:
		img = Image.open(BytesIO(imagefile.read())).convert('RGB')

		# Run some processing and get back image and data
		ret_img, ret_dta, ret_dta_es, ret_dta_tr, ret_dta_ru, ret_dta_it = run_some_function_using_image_as_input(img)

		# Return image and data
		ret_imgio = BytesIO()
		ret_img.save(ret_imgio, 'PNG')

		# Instead of generating a response to a client (flask.wrapper.response)

		#ret_imgio.seek(0)
		#processed_file = send_file(ret_imgio, 
		#	attachment_filename='processed_img.png',
		#	mimetype='image/png')

		# We use the base64 encoded string to display it in the HTML page
		png_output = base64.b64encode(ret_imgio.getvalue())
		processed_file = urllib.parse.quote(png_output)

		print("Image: %s classified as %s" % (imagefile.filename, ret_dta))

	except Exception as err:

		print(err)

		error_msg = "Please only upload .png, .jpg or .jpeg files"

	return render_template('layout.html', **locals())

#def ms_translate_call(toLang, textTranslate, fromLang="en"):
#
#	""" API call to MS Cognitive Services, Translation tool """
#    
#    # Get token
#    acc_key = "SECRET"
#    headers = {"Ocp-Apim-Subscription-Key": acc_key}
#    tok_url = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken"
#    
#    r_tok = requests.post(tok_url, headers=headers).text  
#    
#    # Request for translation
#    headers = {"Authorization ": "Bearer " + r_tok}
#    translateUrl = "http://api.microsofttranslator.com/v2/Http.svc/Translate?text={}&from={}&to={}".format(
#        textTranslate, fromLang, toLang)
#
#    r_trans = requests.get(translateUrl, headers=headers)
#    rsp = r_trans.text
#    soup = BeautifulSoup(rsp, "lxml")
#    return soup.string


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005)