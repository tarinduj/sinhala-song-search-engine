from flask import Flask, render_template, request

from searchapp.data import all_songs
from searchapp.app.search import search

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    """
    Search for products across a variety of terms, and show 9 results for each.
    """
    search_terms = [
        'අම්මා',
        'සෙනෙහස',
        'හදවත',
        'ආදරේ',
        'කුවේණි'
    ]

    num_results = 9
    products_by_category = [(t, search(t, num_results)) for t in search_terms]
    return render_template(
        'index.html',
        products_by_category=products_by_category,
    )


@app.route('/search', methods=['GET', 'POST'])
def search_single_product():
    """
    Execute a search for a specific search term.

    Return the top 50 results.
    """
    query = request.args.get('search')
    artist_name = request.args.get('artist_name')
    album_name = request.args.get('album_name')
    num_results = 50
    products_by_category = [(query, search(query, num_results, artist_name, album_name))]
    return render_template(
        'index.html',
        products_by_category=products_by_category,
        search_term=query,
        artist_name=artist_name,
        album_name=album_name
    )


@app.route('/product/<int:product_id>')
def single_product(product_id):
    """
    Display information about a specific product
    """

    product = str(all_songs()[product_id - 1])

    return render_template(
        'product.html',
        product_json=product,
        search_term='',
    )
