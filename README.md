# Shis

Turn a markdown document into slides.

For instance to upload to instagram.

First separate the document with `---`.

Each `---` defines where a slide ends.

Just provide the path if the .md document and the name of the project.

For instance: `python main.py /path/to/stuff.md stuff`

Then it will create a `stuff/` dir in the dir of the document.

Inside this dir it will save all the images.

The font size of the slides get reduced automatically until it fits.

So if a slide has too much text it might look small.

Run `nix develop` first.