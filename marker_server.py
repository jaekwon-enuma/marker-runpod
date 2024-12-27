import os
import base64
import runpod
import tempfile

# Marker imports
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered

# Prepare the converter on load
converter = PdfConverter(artifact_dict=create_model_dict())

def handler(event):
    """
    Convert a PDF (passed in base64) to text/images via Marker package.
    Expected input format in event["input"]:
      {
         "pdf_base64": "<base64-encoded string>",
      }
    """

    input_data = event.get("input", {})

    pdf_base64 = input_data.get("pdf_base64")
    if not pdf_base64:
        return {"error": "No 'pdf_base64' found in input."}

    fd, temp_filepath = tempfile.mkstemp(suffix=".pdf")

    try:
        with open(temp_filepath, "wb") as f:  # Use the file path, not the file descriptor
            f.write(pdf_bytes)

        rendered = converter(temp_filepath)
        text, metadata, images = text_from_rendered(rendered)

        return {
            "markdown": text,
            "images": images,
            "metadata": metadata
        }

    finally:
        os.close(fd)
        os.remove(temp_filepath)


if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})


