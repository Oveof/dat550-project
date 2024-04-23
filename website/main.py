START_PORT = 8000

from copy import deepcopy
import hashlib
from flask import Flask, request, jsonify , render_template
import socket
from PIL import Image
import http.client
import json
from waitress import serve
import torch
import base64
import io



import numpy as np
import faiss
from transformers import CLIPProcessor, CLIPModel, CLIPImageProcessor, CLIPTokenizerFast
from datasets import load_dataset, load_from_disk

model_name = "openai/clip-vit-base-patch32"

model = CLIPModel.from_pretrained(model_name)
processor = CLIPProcessor.from_pretrained(model_name)
image_processor = CLIPImageProcessor.from_pretrained(model_name)
tokenizer = CLIPTokenizerFast.from_pretrained(model_name)
dataset = load_dataset("tomytjandra/h-and-m-fashion-caption", split="train")
print(dataset)
image_index = faiss.read_index("image_embeddings.index")


def bind_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = START_PORT
    while True:
        try:
            s.bind(("127.0.0.1",port))
            break
        except:
            port += 1
    s.close()
    return port

def render_suggestion(imageb64, text, score):
    return f"""
    <div class="recommendation">
        <h3> Recommended image: </h3>
        <image src="data:image/jpeg;base64,{imageb64}"/>
        <p class="stats"> Score: {score:.2f} </p>
    </div>
    """



my_port = bind_socket()

app = Flask(__name__)


def get_suggestions(image = None, text = None):
    # Should return an array of type [(image,text,score_text,score_image,score_total)]

    print(type(image), type(text))
    output = None

    if image and text and not text.isspace():
        input = processor(text=[text] if text else [], images=[image] if image else [], padding="max_length", truncation=True, return_tensors="pt")
        output = model(**input)
        query = torch.lerp(output.image_embeds, output.text_embeds, 0.5)
    elif image:
        input = image_processor(images=[image], return_tensors="pt")
        output = model.get_image_features(**input)
        query = output
    else:
        input = tokenizer(text=[text], padding="max_length", return_tensors="pt")
        output = model.get_text_features(**input)
        query = output

    query = query.detach().numpy()
    
    faiss.normalize_L2(query)

    k = 5
    D, I = image_index.search(query, k)

    products = []
    for i, product in enumerate(dataset.select(I.flatten())):
        products.append((product["image"], product["text"], D[0][i]))

    return products


@app.route('/search', methods=['POST'])
def handle_upload():
    input_text = None
    input_image = None
    
    if 'text' in request.form:
        input_text = request.form['text']  # Filter out no alphabetical characters

    if 'image' in request.files:
        image = request.files['image']  # Access the file
        input_image = Image.open(image).convert("RGB")


    html = "<div class='responses'>"
    for image, text, score in get_suggestions(input_image, input_text):
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        imageb64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        html+= render_suggestion(imageb64=imageb64, text=text, score=score)
    html+="</div>"
    return html


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    # app.run(host='127.0.0.1', port=my_port,debug=False)
    serve(app, host='0.0.0.0', port=8000) # Production run

## To get auto reload use:
# flask --app main.py --debug run
