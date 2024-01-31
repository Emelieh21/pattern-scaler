from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from reportlab.pdfgen import canvas
import os

from app.utils.functions import scale_pattern

app = FastAPI()

@app.get("/generate_pdf")
def generate_pdf():
    # Generate a simple PDF
    pdf_path = "output.pdf"
    with open(pdf_path, "wb") as pdf_file:
        pdf = canvas.Canvas(pdf_file)
        pdf.drawString(100, 750, "Hello, this is a dynamically generated PDF!")
        pdf.save()

    original_width=123
    original_height=234
    new_width=1234
    new_height=12345

    # Custom headers
    custom_headers = {
        "Content-Disposition": "attachment; filename=output.pdf",
        "X-original-width": f"{original_width}",
        "X-original-height": f"{original_height}",
        "X-new-width": f"{new_width}",
        "X-new-height": f"{new_height}"
    }

    # Return a FileResponse
    return FileResponse(pdf_path, media_type='application/pdf', headers=custom_headers)
    #return FileResponse(pdf_path, media_type='application/pdf', filename='output.pdf')

@app.post("/scale_pattern")
async def upload_file(desired_height: int = 43,
                      desired_width: int = None,
                      scale_factor_height: int = None,
                      scale_factor_width: int = None,
                      line_width: int = None,
                      pdf_resolution: int = 300,
                      file: UploadFile = File(...)):
    
    # Check if the uploaded file is a PNG or PDF
    if file.content_type.lower() not in {"image/png", "application/pdf"}:
        return {"error": "Invalid file type. Please upload a PNG or PDF file."}
    
    # Get the content of the file
    file_content = await file.read()

    # Save the file to the specified path
    with open(file.filename, "wb") as file_output:
        file_output.write(file_content)

    # Execute pattern scaling functionality...
    result_headers = scale_pattern(
                           input_file=file.filename, 
                           desired_height=desired_height, 
                           desired_width=desired_width, 
                           scale_factor_height=scale_factor_height, 
                           scale_factor_width=scale_factor_width, 
                           pdf_resolution=pdf_resolution, 
                           line_width=line_width
                        )
    
    return FileResponse(os.getcwd()+"/app/output-files/result.pdf", media_type='application/pdf', headers=result_headers)

# curl -X POST -H "Content-Type: multipart/form-data" -F "file=@sweater-top.png" "http://localhost:8001/upload_file?desired_height=42"
# curl -X POST -H "Content-Type: multipart/form-data" -F "file=@sweater-top.png" "http://localhost:8001/scale_pattern?desired_height=42"