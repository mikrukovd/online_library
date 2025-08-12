import json

from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape

with open("meta_data.json", "r", encoding="utf8") as my_file:
    #books = my_file.read()
    books = json.load(my_file)

env = Environment(
    loader=FileSystemLoader("."),
    autoescape=select_autoescape(["html"])
)
template = env.get_template("template.html")

rendered_page = template.render(books=books)

'''for book in books:
    #print(book)
    title = book["title"]
    author = book["author"]
    image = book["img_src"]
'''

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
