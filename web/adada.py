
import sys
import importlib

from flask import Flask, render_template, request
import helpers

import numpy as np
import pandas as pd
from time import time


app = Flask(__name__)
#model = helpers.get_model("web/static/W2V.model")
#data = pd.read_pickle("static/reduced_bonus.pkl")
print("path >",app.instance_path)
@app.route("/", methods=["GET","POST"])
def index():
    if request.method=="GET":
          return render_template("index.html",original="", found = "")


    prompt = request.form["prompt"]

    return render_template("index.html",original=prompt, found = get_similar_quote(prompt, model) )


@app.route("/bonus", methods=["GET","POST"])
def bonus():

    return render_template("bonus.html", original="test1", found = "test2")


def extract_extremes(data, column="compound", threshold=15):
    bounds = np.percentile(data[column], (threshold, 100 - threshold))
    return bounds, data[(data[column] < bounds[0]) | (data[column] > bounds[1])]

def get_similar_quote(quote, model):
  ## big overhead here can we compute it only once ?
  start = time()

  print(f"init took {round(time() - start, 2)} s")
  start = time()
  vec_space = np.vstack(data.vectors.values)
  vec = helpers.aggregate(model, helpers.preprocess_quote(quote))

  dists = helpers.__dist(model, vec, vec_space)
  closest_idx = np.argmin(dists)
  quote_entry = data.iloc[closest_idx]
  speaker = quote_entry.speaker
  quote = quote_entry.quotation

  quote_point = vec.reshape((1, -1))
  print(f"processing took {round(time() - start, 2)} s")
  start = time()
  helpers.show_quote_in_set(vec_space, dimensions=2, colors=helpers.get_cmap_from_labels(data.compound.values), quote_point=quote_point, show=False)
  print(f"displaying took {round(time() - start, 2)} s")
  return speaker, quote