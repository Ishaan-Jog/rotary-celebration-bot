from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps


POSTER_WIDTH = 1080


def wrap_text(text, max_chars=25):

    words = text.split()

    lines = []
    current = ""

    for word in words:

        test = (
            current + " " + word
        ).strip()

        if len(test) <= max_chars:
            current = test

        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def draw_centered_text(
    draw,
    text,
    y,
    font,
    fill,
    image_width=POSTER_WIDTH
):

    bbox = draw.textbbox(
        (0, 0),
        text,
        font=font
    )

    width = bbox[2] - bbox[0]

    x = (
        image_width - width
    ) / 2

    draw.text(
        (x, y),
        text,
        font=font,
        fill=fill
    )


def draw_wrapped_text(
    draw,
    text,
    start_y,
    font,
    fill,
    max_chars=25,
    line_gap=70
):

    lines = wrap_text(
        text,
        max_chars
    )

    for i, line in enumerate(lines):

        draw_centered_text(
            draw,
            line,
            start_y + i * line_gap,
            font,
            fill
        )

    return (
        start_y +
        len(lines) * line_gap
    )


def draw_left_wrapped_text(
    draw,
    text,
    x,
    start_y,
    font,
    fill,
    max_chars=25,
    line_gap=90
):

    lines = wrap_text(
        text,
        max_chars
    )

    for i, line in enumerate(lines):

        draw.text(
            (x, start_y + i * line_gap),
            line,
            font=font,
            fill=fill
        )

    return (
        start_y +
        len(lines) * line_gap
    )


def create_photo(
    photo_path,
    width,
    height
):

    photo = Image.open(
        photo_path
    ).convert("RGB")

    photo = ImageOps.fit(
        photo,
        (width, height),
        method=Image.Resampling.LANCZOS
    )

    return photo


def generate_poster(
    event_type,
    name,
    date,
    photo_path
):

    event_type = (
        event_type.lower()
        .strip()
    )

    # ------------------------
    # BIRTHDAY
    # ------------------------

    if "birthday" in event_type:

        template = Image.open(
            "templates/birthday_template.png"
        ).convert("RGBA")

        photo = create_photo(
            photo_path,
            451,
            720
        )

        template.paste(
            photo,
            (49, 201)
        )

        name_y = 620
        date_y = 760

        name_font = ImageFont.truetype(
            "fonts/Poppins-Bold.ttf",
            52
        )

        date_font = ImageFont.truetype(
            "fonts/Poppins-Regular.ttf",
            36
        )

        fill = "#4b2f1f"

        draw = ImageDraw.Draw(
            template
        )

        last_y = draw_left_wrapped_text(
            draw,
            name,
            x=550,
            start_y=620,
            font=name_font,
            fill=fill,
            max_chars=20
        )

        draw_left_wrapped_text(
            draw,
            date,
            x=650,
            start_y=last_y + 20,
            font=date_font,
            fill=fill,
            max_chars=20
        )

        output_file = (
            "generated/poster.png"
        )

    # ------------------------
    # ANNIVERSARY
    # ------------------------

    else:

        template = Image.open(
            "templates/anniversary_template.png"
        ).convert("RGBA")

        photo = create_photo(
            photo_path,
            1080,
            690
        )

        template.paste(
            photo,
            (0, 135)
        )

        draw = ImageDraw.Draw(
            template
        )

        name_font = ImageFont.truetype(
            "fonts/GreatVibes-Regular.ttf",
            100
        )

        date_font = ImageFont.truetype(
            "fonts/Poppins-Regular.ttf",
            50
        )

        fill = "#a67c52"

        last_y = draw_left_wrapped_text(
            draw,
            name,
            x=60,
            start_y=1080,
            font=name_font,
            fill=fill,
            max_chars=20
        )

        last_y = draw_left_wrapped_text(
            draw,
            date,
            x=500,
            start_y=1550,
            font=date_font,
            fill=fill,
            max_chars=25
        )

        output_file = (
            "generated/poster.png"
        )

    template.save(
        output_file
    )

    return output_file