from flask import Flask, render_template, request, send_file
from io import BytesIO
from PIL import Image
import base64
import urllib.parse

app = Flask(__name__)
 
@app.route("/")
def index():
    return render_template('layout.html')

@app.route("/uploader", methods=['POST'])
def upload_file():
	# Get image from upload and stream into PIL object
	imagefile = request.files['imagefile']

	if imagefile and we_like_this_file(imagefile.filename):

		img = Image.open(BytesIO(imagefile.read()))

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

	""" This function requires a PIL Image and performs some 
	processing. It returns an image and some text.

	Eventually the code here could be replaced with a neural network
	that outputs an image with detected objects highlighted and lists
	what they are.

	Basically it's a boring place-holder
	"""

	# Convert grayscale
	img = img.convert('L')

	# Resize
	desired_width = 500
	w_ratio = desired_width/img.size[0]
	calc_length = int((img.size[1])*w_ratio)

	out_img = img.resize((desired_width, calc_length), Image.ANTIALIAS)
	some_dta = ("Converted width: %i px and converted height %i px" % (desired_width, calc_length))
	return out_img, some_dta


if __name__ == "__main__":
    app.run()