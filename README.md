# Shis

Turn standard Markdown documents into perfectly formatted, equal-sized slide images—ideal for Instagram carousels and social media presentations.

Shis automatically handles text overflow: if a slide contains too much text to fit inside the standard vertical frame, the engine intelligently scales the font size down until everything fits perfectly on a single image.

## 🧟‍♀️ Usage

### 1. Format your Markdown
Write your content in a standard `.md` file. Separate each slide using a horizontal rule (`---`).

```markdown
# Slide 1
This is the first image in the carousel.

---

# Slide 2
This text will appear on the second image.
If I write a massive amount of text here, Shis will automatically shrink the font size so it all fits without getting cut off!
```

### 2. Enter the Environment
Because Shis relies on low-level rendering libraries, it uses a Nix flake to guarantee a clean, reproducible environment. Initialize it first:

```bash
nix develop
```

### 3. Generate the Slides
Run the script by providing the path to your Markdown file and the desired name for your output folder.

```bash
python main.py /path/to/stuff.md stuff
```

The script will automatically create a directory named `stuff/` in the same location as your `.md` file and populate it with your generated `slide_1.png`, `slide_2.png`, etc.

## 🪅 How it Works

Most HTML-to-Image tools require installing massive, heavy browser engines like Chromium or Playwright to take screenshots. Shis avoids this entirely by using a lightweight, native rendering pipeline.

1. **Parsing:** The script reads the Markdown file and splits it into discrete HTML blocks based on the `---` dividers.
2. **Auto-Scaling Layout:** It feeds the HTML to a layout engine set to a strict canvas size (e.g., 1080x1350 for Instagram). If the text overflows onto a "second page", a loop triggers that mathematically reduces the base font size by 1 pixel at a time. It continuously re-renders until the engine confirms the text perfectly fits onto a single page.
3. **Rasterization:** Once the perfect font size is found, the layout is exported as a temporary vector PDF, which is instantly rasterized into a crisp PNG image.

## 🐔 Technologies Leveraged

* **Python:** Core scripting, file routing, and logic orchestration.
* **WeasyPrint:** A powerful, lightweight layout engine that converts HTML/CSS into paginated PDFs. This replaces the need for headless web browsers, handling the complex text-wrapping and CSS flexible box layouts natively.
* **PyMuPDF (`fitz`):** A high-performance C-based PDF rasterizer used to convert WeasyPrint's vector output into the final pixel-perfect `.png` files.
* **Nix:** Provides an isolated, reproducible development shell (`nix develop`). This is crucial because WeasyPrint requires complex system-level C libraries (like Cairo and Pango) for text rendering, which Nix handles silently without polluting the host operating system.