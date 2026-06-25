import re
import argparse
from pathlib import Path
import markdown
import weasyprint
import fitz  # PyMuPDF

def generate_carousel(md_filepath, output_subdir_name):
    md_path = Path(md_filepath)

    if not md_path.is_file():
        print(f"Error: File '{md_filepath}' not found.")
        return

    out_dir = md_path.parent / output_subdir_name
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(md_filepath, "r", encoding="utf-8") as f:
        md_text = f.read()

    styles = []

    def style_replacer(match):
        styles.append(match.group(1))
        return ""

    text_no_styles = re.sub(r'<style>(.*?)</style>', style_replacer, md_text, flags=re.DOTALL)
    raw_slides = re.split(r'\n---\n?', text_no_styles)
    user_styles = "\n".join(styles)

    for index, slide in enumerate(raw_slides):
        slide_content = slide.strip()

        if len(slide_content) > 0:
            html_snippet = markdown.markdown(slide_content)
            font_size = 60
            lines = [line for line in slide_content.splitlines() if len(line.strip()) > 0]
            single_line_css = ""

            if len(lines) == 1:
                single_line_css = """
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    text-align: center;
                    height: 1270px;
                """

            while True:
                html_document = f"""
                <!DOCTYPE html>
                <html>

                <head>
                    <meta charset="utf-8">
                    <style>
                        @page {{
                            size: 1080px 1350px;
                            margin: 0;
                        }}

                        body {{
                            margin: 0;
                            padding: 40px;
                            background-color: #0d1117;
                            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                            color: #e6edf3;
                            font-size: {font_size}px;
                            {single_line_css}
                        }}

                        h1 {{ font-size: 2.2em; color: #58a6ff; margin-top: 0; margin-bottom: 0.5em; }}
                        h2 {{ font-size: 1.8em; color: #58a6ff; margin-top: 0; margin-bottom: 0.5em; }}
                        p {{ font-size: 1em; line-height: 1.5; margin-bottom: 1em; }}

                        blockquote {{
                            margin: 0.2em 0 0.5em 0;
                            padding: 0 0 0 0.6em;
                            border-left: 0.2em solid #484f58;
                            color: #e6edf3;
                            font-style: italic;
                        }}

                        img {{
                            max-width: 100%;
                            max-height: 600px;
                            object-fit: contain;
                            border-radius: 12px;
                            display: block;
                            margin: 1em auto;
                        }}

                        {user_styles}
                    </style>
                </head>

                <body>
                    {html_snippet}
                </body>

                </html>
                """

                doc = weasyprint.HTML(
                    string=html_document,
                    base_url=str(md_path.parent)
                ).render()

                if len(doc.pages) == 1:
                    pdf_bytes = doc.write_pdf()
                    break

                if font_size <= 12:
                    pdf_bytes = doc.write_pdf()
                    break

                font_size -= 1

            output_name = out_dir / f"slide_{index + 1}.png"
            pdf_doc = fitz.open("pdf", pdf_bytes)
            page = pdf_doc[0]
            mat = fitz.Matrix(96 / 72, 96 / 72)
            pix = page.get_pixmap(matrix=mat)
            pix.save(str(output_name))
            print(f"Generated: {output_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Instagram Carousel from Markdown")
    parser.add_argument("md_file", help="Path to the markdown file")
    parser.add_argument("out_dir", help="Name of the output subdirectory")
    args = parser.parse_args()
    generate_carousel(args.md_file, args.out_dir)