from jinja2 import Environment
from jinja2 import FileSystemLoader
import os
from datetime import datetime


def render_template(
    name,
    photo_path,
    event_type,
    date
):

    env = Environment(
        loader=FileSystemLoader(
            "templates"
        )
    )

    template = env.get_template(
        "birthday.html"
    )

    phrase = (
        "Wishing you joy and happiness!"
    )

    html = template.render(
        name=name,
        photo_url=photo_path,
        phrase=phrase,
        event_type=event_type,
        date=date
    )

    output_file = (
        "generated/poster.html"
    )

    print(photo_path)
    print(os.path.exists(photo_path))
    print(os.path.getsize(photo_path))

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)

    return output_file