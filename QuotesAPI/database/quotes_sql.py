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


import shortuuid
import random

from threading import RLock
from QuotesAPI import DB_URI

from sqlalchemy import Column, String, UnicodeText
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


# SQLAlchemy declarative base obj
Base = declarative_base()


class MCUQuotes(Base):
    __tablename__ = "mcu_quotes"
    id = Column(String, primary_key=True)
    character = Column(UnicodeText, nullable=False)
    quote = Column(UnicodeText, nullable=False)

    def __init__(self, id, character, quote):
        self.id = id
        self.character = character
        self.quote = quote

    def __repr__(self):
        return f"id={self.ud}, character={self.character}, quote={self.quote}"


class DCUQuotes(Base):
    __tablename__ = "dcu_quotes"
    id = Column(String, primary_key=True)
    character = Column(UnicodeText, nullable=False)
    quote = Column(UnicodeText, nullable=False)

    def __init__(self, id, character, quote):
        self.id = id
        self.character = character
        self.quote = quote

    def __repr__(self):
        return f"id={self.ud}, character={self.character}, quote={self.quote}"


class SuperHeroQuotesDB:
    """
    The main database class, which does the following:

    * creates table for SQL database if not exists.
    * starts database connection using scoped session.
    * fetches and loads quotes from database into memory.
    * holds all methods to fetch/insert/delete quotes.

    """

    def __init__(self):
        self._dcu_quotes = []
        self._mcu_quotes = []
        self._session = self._start_session()
        self._lock = RLock()
        self.__reload_quotes()  # load quotes in memory

    @property
    def total(self):
        """
        Returns total number of quotes in database.
        """
        return len(self._dcu_quotes + self._mcu_quotes)

    @property
    def all(self):
        """
        Returns list of all quotes from database.
        """
        return self._mcu_quotes + self._dcu_quotes

    @staticmethod
    def _start_session() -> scoped_session:
        """Creates SQLAlchemy scoped session."""
        engine = create_engine(DB_URI, client_encoding="utf8")
        Base.metadata.bind = engine
        Base.metadata.create_all(engine)

        # create database tables if not exist already
        MCUQuotes.__table__.create(checkfirst=True)
        DCUQuotes.__table__.create(checkfirst=True)

        return scoped_session(sessionmaker(bind=engine, autoflush=False))

    def get_quotes(self, cat, size=10):
        """Get quotes for category with size limit."""

        cat = cat.lower()
        if cat in {"mcu", "dcu"}:
            if cat == "mcu":
                results = random.sample(self._mcu_quotes, size)
            elif cat == "dcu":
                results = random.sample(self._dcu_quotes, size)

            banner = (
                "Marvel Cinematic Universe (MCU)"
                if cat == "mcu"
                else "DC Universe (DCU)"
            )
            jsondata = {
                "StatusCode": 200,
                "Banner": banner,
                "TotalQuotes": len(results),
                "Items": results,
            }
            return jsondata

        return None

    def quote_by_id(self, qid):
        """Get specific quote with it's id"""

        all_quotes = self._mcu_quotes + self._dcu_quotes
        quote = next((item for item in all_quotes if item["id"] == qid), None)
        if quote:
            return {"StatusCode": 200, "Stuff": quote}
        return None

    def ramdom_quote(self):
        """Get random quotes from both dc & marvel collection"""

        r_banner = random.choice([self._mcu_quotes, self._dcu_quotes])
        b_name = (
            "Marvel Cinematic Universe (MCU)"
            if r_banner is self._mcu_quotes
            else "DC Universe (DCU)"
        )
        return {
            "StatusCode": 200,
            "Banner": b_name,
            "Stuff": random.choice(r_banner),
        }

    def insert(self, char, quote, table):
        """Insert quotes in database."""

        with self._lock:
            table = MCUQuotes if table == "mcu" else DCUQuotes
            qid = shortuuid.uuid()
            check = self._session.query(table).get(qid)

            if not check:
                addr = table(qid, char, quote)
                self._session.add(addr)
                self._session.commit()
                return True

            self._session.close()
            return False

    def delete(self, qid, table):
        """Delete quote with the id from DB"""

        with self._lock:
            table = MCUQuotes if table == "mcu" else DCUQuotes
            curr = self._session.query(table).get(qid)
            if curr:
                self._session.delete(curr)
                self._session.commit()
                return True

            self._session.close()
            return False

    def __reload_quotes(self):
        """
        Load all quotes in memory for faster access.
        """

        try:
            mcu = self._session.query(MCUQuotes).all()
            dcu = self._session.query(DCUQuotes).all()

            for x in mcu:
                self._mcu_quotes.append(
                    {
                        "id": x.id,
                        "data": {"author": x.character, "quote": x.quote},
                    }
                )

            for x in dcu:
                self._dcu_quotes.append(
                    {
                        "id": x.id,
                        "data": {"author": x.character, "quote": x.quote},
                    }
                )
        finally:
            self._session.close()

    def __repr__(self):
        return f"{self.__class__.__name__}(total={self.total})"
