import re
import argparse
import base64
from io import BytesIO
from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage
from pdf2image import convert_from_path

def encode_image(pil_image):
    buffer = BytesIO()
    pil_image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

def prompt_template(image_base64):
    prompt_template = HumanMessage(
        content=[
            {"type": "text", "text": "Perform Optical Character Recognition (OCR) on the following image and extract the text. The text should be formatted in Markdown, inside a code block with three back ticks"},
            {"type": "image_url", "image_url": f"data:image/png;base64,{image_base64}"}
        ]
    )
    return prompt_template

def sanitize_llm_answer(answer: str) -> str:
    if "```" in answer:
        return re.search(r"```(?:\w+\n)?(.*?)```", answer, re.DOTALL).group(1)
    else:
        return answer

def ocr(args):
    model = ChatOllama(
        model=args.model
    )

    pdf_pages = convert_from_path(args.path)
    b64_images = [encode_image(image) for image in pdf_pages]

    for img in b64_images:
        result = model.invoke([prompt_template(img)])
        return sanitize_llm_answer(result.content)

def main(args):
    print(ocr(args))

if __name__=="__main__":
    parser = argparse.ArgumentParser()

    # parser.add_argument(
    #     "--model",
    #     type=str,
    #     help="VLM model to use for OCR"
    # )

    parser.add_argument(
        "--temperature",
        default=0.1,
        type=float,
        help="Temperature to be set for decoding"
    )

    parser.add_argument(
        "--top-p",
        default=0.9,
        type=float,
        help="Top-P value to use"
    )

    parser.add_argument(
        "--top-k",
        default=40,
        type=int,
        help="Top-K value to use"
    )

    parser.add_argument(
        "--path",
        type=str,
        help="Path to PDF"
    )

    args = parser.parse_args()

    main(args)