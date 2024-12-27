import io
import os
import base64
import zipfile
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

    print("handler 01", flush=True)
    input_data = event.get("input", {})
    print("handler 02", flush=True)

    pdf_base64 = input_data.get("pdf_base64")
    if not pdf_base64:
        return {"error": "No 'pdf_base64' found in input."}

    print("handler 03", flush=True)
    fd, temp_filepath = tempfile.mkstemp(suffix=".pdf")

    try:
        print("handler 04", flush=True)
        # Decode the base64 content
        pdf_bytes = base64.b64decode(pdf_base64)

        with io.BytesIO(zip_bytes) as zbuf:
            with zipfile.ZipFile(zbuf, "r") as zipf:
                # Assuming the PDF inside the zip is stored as 'document.pdf'
                pdf_bytes = zipf.read("document.pdf")

        # Write the decoded bytes to a temporary file
        with open(temp_filepath, "wb") as f:
            f.write(pdf_bytes)

        print("handler 05", flush=True)
        rendered = converter(temp_filepath)
        print("handler 06", flush=True)
        markdown_text, metadata, images = text_from_rendered(rendered)
        print(f"handler 07 len:{len(markdown_text)}", flush=True)

        images_base64 = {}
        for image_name, image_obj in images.items():
            print(f"image 0 {image_name}")
            # Save image to in-memory bytes buffer
            buf = io.BytesIO()
            image_obj.save(buf, format="JPEG")
            buf.seek(0)

            print(f"image 1 {image_name}")
            # Base64-encode the image data
            encoded_image = base64.b64encode(buf.read()).decode("utf-8")
            print(f"image 2 {image_name}")
            images_base64[image_name] = encoded_image
            print(f"image 3 {image_name}")

        print(f"Sending images {len(images_base64)}")
        return {
            "markdown": markdown_text,
            "metadata": metadata,
            "images": images_base64  # Each value is a Base64-encoded string
        }

    finally:
        os.close(fd)
        os.remove(temp_filepath)


if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})


