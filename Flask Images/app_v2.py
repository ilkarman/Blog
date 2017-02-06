from flask import Flask, render_template, request, send_file
from io import BytesIO
from PIL import Image
import base64
import urllib.parse
# Additions for image classification
import mxnet as mx
import numpy as np
from collections import namedtuple
import time

Batch = namedtuple('Batch', ['data'])

app = Flask(__name__)
 
@app.route("/")
def index():
    return render_template('layout.html')

@app.route("/uploader", methods=['POST'])
def upload_file():
	# Get image from upload and stream into PIL object
	imagefile = request.files['imagefile']

	if imagefile and we_like_this_file(imagefile.filename):

		img = Image.open(BytesIO(imagefile.read())).convert('RGB')

		# Remove the alpha channel (want R, G, B)
		print("Image channels: ", len(img.split()))
		print("Image mode: ", img.mode)
		#if imagefile.filename.split('.')[-1] == "png":
		#	img.load()
		#	img_no_alpha = Image.new("RGB", img.size, (255, 255, 255))
		#	img_no_alpha.paste(img, mask=img.split()[3])
		#	img = img_no_alpha

		# Run some processing and get back image and data
		ret_img, ret_dta = run_some_function_using_image_as_input(img)

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

	else:

		error_msg = "Please only upload .png, .jpg or .jpeg files"

	return render_template('layout.html', **locals())

def we_like_this_file(fname):
	ok_extensions = set(['png', 'jpg', 'jpeg'])
	if fname.split('.')[-1] in ok_extensions:
		return True
	return False

def run_some_function_using_image_as_input(img):

	# Load image
	img = img.resize((224, 224), Image.ANTIALIAS)
	
	# Change shape
	img_np = np.swapaxes(img, 0, 2)
	img_np = np.swapaxes(img_np, 1, 2) 
	img_np = img_np[np.newaxis, :] 

 	# Load model and labels
	with open('synset.txt', 'r') as f:
	    synsets = [l.rstrip() for l in f]

	sym, arg_params, aux_params = mx.model.load_checkpoint('resnet-152', 0)

	# Create model
	mod = mx.mod.Module(symbol=sym, context=mx.cpu())
	mod.bind(for_training=False, data_shapes=[('data', (1,3,224,224))])
	mod.set_params(arg_params, aux_params)
  
	# Prediction
	mod.forward(Batch([mx.nd.array(img_np)]))
	prob = mod.get_outputs()[0].asnumpy()
	prob = np.squeeze(prob)
	
	#time.sleep(10)

	# Category
	a = np.argsort(prob)[-1]    
	classification = " ".join(synsets[a].split(" ")[1:]).split(",")[0]

	return img, classification


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005)