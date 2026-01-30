import nbformat
import sys
import base64
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Convert .ipynb to Markdown")
    parser.add_argument("input", help="Path to the notebook file")
    parser.add_argument(
        "--local", 
        action="store_true", 
        help="Save images to a local folder instead of embedding base64"
    )
    
    args = parser.parse_args()
    nb_path = Path(args.input)
    
    if not nb_path.exists():
        print(f"Error: File {args.input} not found.")
        return

    output_dir = nb_path.parent / f"{nb_path.stem}_media"
    md_output = nb_path.with_suffix(".md")
    
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    markdown_lines = []

    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            markdown_lines.append(cell.source + "\n")
            
        elif cell.cell_type == 'code':
            markdown_lines.append(f"```python\n{cell.source}\n```\n")
            
            for output in cell.get('outputs', []):
                # 1. Text output
                if output.output_type == 'stream':
                    markdown_lines.append(f"```text\n{output.text.strip()}\n```\n")
                
                # 2. Results and Images
                elif output.output_type in ['execute_result', 'display_data']:
                    data = output.get('data', {})
                    
                    if 'text/plain' in data:
                        markdown_lines.append(f"```text\n{data['text/plain'].strip()}\n```\n")
                    
                    # Handle Images (PNG and JPEG)
                    for fmt in ['image/png', 'image/jpeg']:
                        if fmt in data:
                            b64_str = data[fmt].replace('\n', '')
                            mime_type = fmt
                            
                            if args.local:
                                # SAVE LOCALLY
                                if not output_dir.exists():
                                    output_dir.mkdir(parents=True)
                                ext = "png" if "png" in fmt else "jpg"
                                img_name = f"image_{len(list(output_dir.glob(f'*.{ext}')))}.{ext}"
                                img_path = output_dir / img_name
                                
                                with open(img_path, 'wb') as f:
                                    f.write(base64.b64decode(b64_str))
                                markdown_lines.append(f"![{img_name}]({output_dir.name}/{img_name})\n")
                            else:
                                # EMBED (Default)
                                markdown_lines.append(f"![embedded image](data:{mime_type};base64,{b64_str})\n")

    with open(md_output, 'w', encoding='utf-8') as f:
        f.write("\n".join(markdown_lines))
    
    mode = "Local" if args.local else "Embedded"
    print(f"Done! Mode: {mode} -> Created {md_output}")

if __name__ == "__main__":
    main()