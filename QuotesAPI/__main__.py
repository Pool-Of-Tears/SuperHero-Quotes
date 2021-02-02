#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (C) 2020-2021 Stɑrry Shivɑm.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""
Restful Superhero QuoteAPI written in python3 with Flask, Falsk-RESTful
and SQLAlchemy database, by (www.github.com/starry69) as fun project.

Also since i actually needed a good MCU and DCU Quotes collection and was looking
for some nice API but didn't found one so decided to make my own, Cause why not!
"""


from flask import Flask, render_template
from flask_restful import Api, Resource, abort, reqparse
from QuotesAPI.database import quot
from QuotesAPI import ACCESS_KEY

app = Flask(__name__, template_folder="../templates", static_folder="../static")
api = Api(app)


class GetRandom(Resource):
    """
    Fetch random quotes from both mcu & dcu banner.
    """

    @staticmethod
    def get():
        return quot.ramdom_quote(), 200


class QuoteByID(Resource):
    """
    Fetch "specific" quote by it's Id
    """

    @staticmethod
    def get(quote_id):
        quote = quot.quote_by_id(quote_id)
        if quote is not None:
            return quote, 200
        abort(404, message="Can't find any quote for this id.")


# request parser for /grab endpoint.
grab_parser = reqparse.RequestParser()
grab_parser.add_argument(
    "banner",
    type=str,
    required=True,
    help="Banner of quotes to look for is required!",
)
grab_parser.add_argument(
    "size",
    type=int,
    required=False,
    help="Optionnal: total numbers of quotes to fetch",
)


class GrabCategory(Resource):
    """Get quotes for the category"""

    @staticmethod
    def get():
        args = grab_parser.parse_args()
        if args["size"] is not None:
            if args["size"] > 50:
                abort(400, message="You can only fetch max 50 quotes at time!")
            data = quot.get_quotes(args["banner"], args["size"])
        else:
            data = quot.get_quotes(args["banner"])

        if data is not None:
            return data, 200

        abort(
            404,
            message="Not found: Invalid banner provided!: Valid banners=['mcu', 'dcu']",
        )


# request parser for /insert endpoint.
insert_parser = reqparse.RequestParser()
insert_parser.add_argument(
    "access_key",
    type=str,
    required=True,
    help="Acess key is required to insert quote in database",
)
insert_parser.add_argument(
    "char",
    type=str,
    required=True,
    help="Charater / author of quote is required!",
)
insert_parser.add_argument(
    "quote", type=str, required=True, help="Quote to insert is required!"
)
insert_parser.add_argument(
    "table",
    type=str,
    required=True,
    help="Table name to insert quotes into is required!",
)


class InsertQuote(Resource):
    """
    Inserts quote in database availabe
    to devlopers only!
    """

    @staticmethod
    def post():
        args = insert_parser.parse_args()

        if args["access_key"] != ACCESS_KEY:
            abort(400, message="Invalid acess key!")

        if args["table"] in {"mcu", "dcu"}:
            quot.insert(
                char=args["char"], quote=args["quote"], table=args["table"]
            )
            return {"message": "Successfully inserted"}, 201

        abort(400, message="table parameter must be either 'dcu' or 'mcu'")


@app.route("/")
def index():
    return render_template("index.html")


api.add_resource(GetRandom, "/random", endpoint="random")
api.add_resource(GrabCategory, "/grab", endpoint="grab")
api.add_resource(QuoteByID, "/quoteId/<string:quote_id>")
api.add_resource(InsertQuote, "/insert", endpoint="insert")


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
