import json
import os
import math

from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked
from dotenv import load_dotenv


def prepare_books(books):
    '''Подготавливает данные для рендера'''
    for book in books:
        book['genres'] = book['genres'].replace('.', '').split(', ')
    return books


def render_pages():
    '''Рендер страниц'''
    with open("meta_data.json", "r", encoding="utf8") as file:
        books = prepare_books(json.load(file))

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html"])
    )
    env.filters["chunked"] = chunked
    template = env.get_template("template.html")

    os.makedirs("pages", exist_ok=True)
    books_per_page = 10
    books_per_row = 2
    chunked_books = list(chunked(books, books_per_page))
    total_pages = math.ceil(len(books) / books_per_page)
    base_path = "/online_library"

    for page_num, book_chunk in enumerate(chunked_books, start=1):
        columns = [
            book_chunk[:len(book_chunk)//books_per_row],
            book_chunk[len(book_chunk)//books_per_row:]
        ]
        rendered_page = template.render(
            columns=columns,
            current_page=page_num,
            total_pages=total_pages,
            base_path=base_path,
        )
        with open(f"pages/index{page_num}.html", "w", encoding="utf8") as file:
            file.write(rendered_page)


def main():
    load_dotenv()
    render_pages()
    server = Server()
    server.watch("template.html", render_pages)

    server.serve(
        root=".", port=5500,
        host="127.0.0.1", default_filename="./pages/index1.html"
    )


if __name__ == "__main__":
    main()
