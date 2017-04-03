#!/usr/bin/env python3

import os
import random
import templates
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from madlibs import MadlibList

PORT = int(os.environ.get("PORT", 5000))

madlibs = MadlibList().madlibs()
MADLIBS = {madlibs.index(madlib): madlib for madlib in madlibs}

def choose_madlib_key():
    keys = [key for key in MADLIBS.keys()]
    return random.choice(keys)

def get_madlib(key):
    return MADLIBS[key]

class MadlibHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.ROUTES = {'/': self.render_main, '/madlib': self.do_form}
        self.POST_ROUTES = {'/madlib': self.build_madlib}
        super().__init__(*args, **kwargs)

    def make_response(self, status, content, content_type="text/html"):
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.send_header("Content-length", len(content))
        self.end_headers()
        self.wfile.write(content)

    def render_template(self, template, status=200):
        self.make_response(status, template.encode())

    def do_GET(self):
        if self.path in self.ROUTES:
            self.render_template(self.ROUTES[self.path]())
        else:
            self.render_template(templates.NOT_FOUND, 404)
    
    def do_POST(self):
        if self.path in self.POST_ROUTES:
            content = self.rfile.read(int(self.headers['Content-Length']))
            self.render_template(self.POST_ROUTES[self.path](content))
        else:
            self.render_template(templates.NOT_FOUND, 404)

    def render_main(self):
        return templates.MAIN

    def build_madlib_form(self, key):
        madlib = get_madlib(key)
        key_str = 'Madlib Key: <input type=text name=key value={key} readonly><br>'.format(key=key)
        input_str = '{split}: <input type="text" name={blank}><br>'
        blanks = [input_str.format(blank=blank, split=" ".join(blank.split('_'))) for blank in madlib.blanks]
        return templates.FORM.format(key=key_str, blanks="".join(blanks))   

    def do_form(self):
        key = choose_madlib_key()
        return self.build_madlib_form(key)

    def build_madlib(self, data):
        inputs = {key: value for key, value in [pair.split('=') for pair in data.decode('utf-8').split('&')]} 
        madlib_key = inputs['key']
        answers = {key: inputs[key] for key in inputs if key != 'key'}
        madlib = get_madlib(int(madlib_key))
        madlib.set_answers(answers)
        return templates.MADLIB.format(madlib=madlib.render())


httpd = TCPServer(("", PORT), MadlibHandler)

print("serving at port", PORT)
httpd.serve_forever()
