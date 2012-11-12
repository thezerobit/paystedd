import cgi
import string
import random
import datetime

import bottle

import pygments
from pygments.lexers import guess_lexer, get_all_lexers
from pygments.formatters import HtmlFormatter

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DB Stuff
DBURL = 'postgresql+psycopg2://paystedduser:paysteddpass@localhost/paystedd'
ENGINE = sa.create_engine(DBURL)
Base = declarative_base()
class Paste(Base):
    __tablename__ = 'pastes'
    id = sa.Column(sa.Integer, primary_key=True)
    slug = sa.Column(sa.Text(length=8), index=True, unique=True, nullable=False)
    payload = sa.Column(sa.Text, nullable=False)
    created = sa.Column(sa.DateTime, nullable=False)
    highlight_type = sa.Column(sa.Text, nullable=False)
Base.metadata.create_all(ENGINE)
Session = sessionmaker(bind=ENGINE)

# HTML
BASE_PAGE = '''<!DOCTYPE html><html><head>
<title>PAYSTEDD</title><style>{0}</style></head>
<body><div>
  <a href="/">new</a>
  <a href="/recent">recent</a>
</div>{1}</body></html>'''
INPUT_FORM = '''<form method="POST" action="/new">
<div><textarea name="payload" rows="24" cols="80"></textarea></div>
<div>Highlight Type: <select name="lexer">
  <option value="">Auto</option>{0}
</select></div>
<div><input type="submit" value="Create" /></div>
</form>'''

# Lexer stuffs
def get_lexer_by_name(name):
    for l in get_all_lexers():
        if l[0] == name:
            return pygments.lexers.get_lexer_by_name(l[1][0])
    raise Exception("Lexer not found: {0}".format(name))
FORMATTER = HtmlFormatter()

@bottle.route('/')
def do_main():
    options = ['<option name="{0}">{0}</option>'.format(cgi.escape(l[0], True))
            for l in sorted(get_all_lexers(), key=lambda x: x[0])]
    options_text = ''.join(options)
    return BASE_PAGE.format('', INPUT_FORM.format(options_text))

@bottle.route('/new', method='POST')
def do_new():
    payload = bottle.request.forms.payload
    which_lexer = bottle.request.forms.lexer
    slug = ''.join([random.choice(string.letters + string.digits)
        for x in range(8)])
    if which_lexer == u'':
        lexer = guess_lexer(payload)
    else:
        lexer = get_lexer_by_name(which_lexer)
    session = Session()
    try:
        paste = Paste(slug=slug, payload=payload,
                created=datetime.datetime.now(),
                highlight_type=lexer.name)
        session.add(paste)
        session.commit()
    finally:
        session.close()
    bottle.redirect('/' + slug)

@bottle.route('/recent')
def get_recent():
    session = Session()
    try:
        recent = session.query(Paste).order_by(sa.desc(Paste.created)).slice(0, 20)
        recent_html = '<ul>{0}</ul>'.format(
                ''.join(['<li><a href="/{0}">{0}</a></li>'.format(
                    cgi.escape(p.slug, True)) for p in recent]))
        return BASE_PAGE.format('', recent_html)
    finally:
        session.close()

@bottle.route('/:slug')
def show_paste(slug):
    session = Session()
    try:
        paste = session.query(Paste).filter_by(slug=slug).first()
        if paste is None:
            bottle.response.status = 404
            return BASE_PAGE.format('', 'Paste Not Found')
        else:
            lexer = get_lexer_by_name(str(paste.highlight_type))
            code = pygments.highlight(paste.payload, lexer, FORMATTER)
            return BASE_PAGE.format(FORMATTER.get_style_defs('.highlight'),
                    code + "<div>Highlight Type: {0}</div>".format(cgi.escape(paste.highlight_type)))
    finally:
        session.close()

if __name__=='__main__':
    bottle.run(host='localhost', port='8080')
