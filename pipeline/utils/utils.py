import json
import re
import copy
import random
import numpy as np
import pandas as pd
from PIL import Image, ImageColor, ImageDraw
from io import StringIO
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def contains_chinese(text):
    # Check if the text contains any Chinese characters
    return bool(re.search("[\u4e00-\u9FFF]", text))


# load the personas
PERSONAS = []
with open("./pipeline/persona.jsonl", "r") as f:
    for line in f:
        if not contains_chinese(line): PERSONAS.append(json.loads(line)["persona"])
        else: continue


def is_json_valid(json_str):
    try:
        obj = json.loads(json_str)
        if not isinstance(obj, dict) and not isinstance(obj, list):
            raise RuntimeError("No valid JSON.")
        return True
    except Exception:
        return False


def extract_json(input_string):
    # Using regex to identify JSON structures in the string
    json_match = re.search(r"(\{.*\}|\[.*\])", input_string, re.DOTALL)
    if json_match:
        extracted_json = json_match.group(0)
        try:
            # Convert the extracted JSON string into a Python dictionary or list of dictionaries
            json.loads(extracted_json)
            return extracted_json
        except json.JSONDecodeError:
            return ""
    else:
        return ""


def extract_code(input_string):
    # extract code from the input string
    code_match = re.search(r"```python(.*)```", input_string, re.DOTALL)
    if code_match:
        extracted_code = code_match.group(1).strip()
        return extracted_code
    else:
        code_match = re.search(r"```(.*)```", input_string, re.DOTALL)
        if code_match:
            extracted_code = code_match.group(1).strip()
            return extracted_code
        else:
            print("No valid code found")
            return None


def extract_latex(input_string):
    # extract code from the input string
    code_match = re.search(r"```latex(.*)```", input_string, re.DOTALL)
    if code_match:
        extracted_code = code_match.group(1).strip()
        return extracted_code
    else:
        code_match = re.search(r"```(.*)```", input_string, re.DOTALL)
        if code_match:
            extracted_code = code_match.group(1).strip()
            return extracted_code
        else:
            print("No valid code found")
            return None


def extract_html(input_string):
    # extract code from the input string
    code_match = re.search(r"```html(.*)```", input_string, re.DOTALL)
    if code_match:
        extracted_code = code_match.group(1).strip()
        return extracted_code
    else:
        code_match = re.search(r"```(.*)```", input_string, re.DOTALL)
        if code_match:
            extracted_code = code_match.group(1).strip()
            return extracted_code
        else:
            print("No valid code found")
            return None


def extract_mermaid(input_string):
    # extract code from the input string
    code_match = re.search(r"```mermaid(.*)```", input_string, re.DOTALL)
    if code_match:
        extracted_code = code_match.group(1).strip()
        return extracted_code
    else:
        code_match = re.search(r"```(.*)```", input_string, re.DOTALL)
        if code_match:
            extracted_code = code_match.group(1).strip()
            return extracted_code
        else:
            print("No valid code found")
            return None


def randomize_matplorlib_code(code):
    lines = code.split("\n")
    new_lines = []
    available_styles = plt.style.available

    styles_for_randomization = []
    for style in available_styles:
        if "dark_background" in style: continue
        else: styles_for_randomization.append(style)
    
    random.seed(len(code))
    random.shuffle(styles_for_randomization)

    for line in lines:
        if "style.use" in line:
            STYLE_IS_VALID = False
            for style in available_styles:
                if style in line:
                    STYLE_IS_VALID = True
                    break
            if not STYLE_IS_VALID:
                indent = len(line) - len(line.lstrip()) # check how many indents are there
                random_style = random.choice(styles_for_randomization)
                new_lines.append(f"{' ' * indent}plt.style.use('{random_style}')")
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    return "\n".join(new_lines)


def is_csv_valid(csv_str):
    try:   
        # return False if there are less than 2 lines
        lines = csv_str.split("\n")
        if len(lines) < 2: return False

        df = pd.read_csv(StringIO(csv_str))
        if not isinstance(df, pd.DataFrame):
            raise RuntimeError("No valid CSV.")
        return True
    except Exception:
        return False


def extract_csv(input_string):
    lines = [line.strip() for line in input_string.split("\n") if "," in line]
    csv = []
    num_columns = None

    for line in lines:
        if line.strip():  # Ignore empty lines
            columns = line.split(",")
            if num_columns is None:
                num_columns = len(columns)
            elif len(columns) != num_columns:
                continue
            csv.append(columns)

    return "\n".join([",".join(row) for row in csv])


def compute_white_px_ratio(image):
    # Compute the ratio of white pixels in the image
    white_px = 0
    total_px = 0
    for px in image.getdata():
        if px == (255, 255, 255):
            white_px += 1
        total_px += 1
    return white_px / total_px


def compute_major_px_ratio(image):
    # Compute the ratio of the most common pixel in the image
    px_count = {}
    for px in image.getdata():
        if px in px_count:
            px_count[px] += 1
        else:
            px_count[px] = 1
    
    max_px = max(px_count, key=px_count.get)
    return px_count[max_px] / len(image.getdata())


def process_image(image, max_size=(2560, 1440), major_px_threshold=0.95, aspect_ratio_threshold=5, filter_small=True):
    # Resize the image if it exceeds the maximum size
    if image.size[0] * image.size[1] > max_size[0] * max_size[1]:
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    # Convert alpha channel to white background
    if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
        alpha = image.convert('RGBA').split()[-1]
        bg = Image.new("RGBA", image.size, (255, 255, 255, 255))
        bg.paste(image, mask=alpha)
        image = bg.convert("RGB")
    else:
        image = image.convert("RGB")
    
    major_px_ratio = compute_major_px_ratio(image)
    if major_px_ratio > major_px_threshold: print("Warning: Image is monochromatic.", major_px_ratio); return None

    byte_array = image.tobytes()
    width, height = image.size

    aspect_ratio = max(width, height) / min(width, height)
    if aspect_ratio > aspect_ratio_threshold: print("Warning: Image aspect ratio is too high."); return None

    if min(width, height) < 128 and filter_small: print("Warning: Image is too small."); return None

    image_from_byte_array = Image.frombytes("RGB", (width, height), byte_array)
    
    return image_from_byte_array


def fix_latex_white_text(code):
    RGB_replacements = ["{128,128,128}",
                        "{41,128,185}",
                        "{0,102,204}",
                        "{255,140,0}",
                        "{34,139,34}",
                        "{102,178,255}",
                        "{144,238,144}",
                        "{240,128,128}",
                        "{221,160,221}",
                        "{255,160,122}"]
    
    HEX_replacements = ["808080",
                        "2980B9",
                        "0066CC",
                        "FF8C00",
                        "228B22",
                        "66B2FF",
                        "90EE90",
                        "F08080",
                        "DDA0DD",
                        "FFA07A"]

    fix = False

    if "{255,255,255}" in code:
        code = code.replace("{255,255,255}", random.choice(RGB_replacements))
        fix = True
    
    if "FFFFFF" in code:
        code = code.replace("FFFFFF", random.choice(HEX_replacements))
        fix = True

    return code, fix