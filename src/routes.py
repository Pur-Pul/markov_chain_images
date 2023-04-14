from flask import (
    render_template,
    redirect,
    request,
    session,
    jsonify,
    make_response,
    flash
)

from app import app
import os
import re
from main import Main

class WebMain(Main):
    def __init__(self, inputs):
        Main.__init__(self)
        self.inputs = inputs
        self.return_data = {}

    def inp(self, prompt, regex):
        if prompt == "Number of input pictures: ":
            return len(self.inputs["Pictures"])
        if prompt == "Enter picture name: ":
            return self.inputs["Pictures"].pop()
        if "Color compression value" in prompt:
            prompt = "Color compression value"

        i = self.inputs[prompt]
        while not re.fullmatch(regex, i):
            print("Invalid input.")
            i = input(prompt)
        return i
    
    def generate_image(self, table, image_width, image_height):
        self.return_data["generated_table"] = table
        self.return_data["generated_height"] = image_height
        self.return_data["generated_width"] = image_width
        self.return_data["rgb_list"] = self.rgb_list

@app.route("/")
def index():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    images = []
    for title in os.listdir(os.path.join(current_dir, "input")):
        images.append(
            {
                "title":title
            }
        )
    return render_template("index.html", images = images)

@app.route("/generate", methods=["POST"])
def generate():
    images=[]
    inputs = {
        "Number of neighbours (8/4): ": "8",
        "Use trie? (Y/N): ": "Y",
        "Enter width of new image: ": "32",
        "Enter height of new image: ": "32",
        "Color compression value": "1",
        "Pictures": []
    }
    for prompt, input in request.form.items():
        if "image_" in prompt:
            images.append(input)
        else:
            inputs[prompt] = input
    inputs["Pictures"] = images
    markov = WebMain(inputs)
    markov.run()
    return render_template("image.html", data=markov.return_data)
