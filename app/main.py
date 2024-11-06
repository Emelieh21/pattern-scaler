from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from reportlab.pdfgen import canvas
import os

from app.utils.functions import scale_pattern

app = FastAPI()

@app.post("/scale_pattern")
async def upload_file(desired_height: float = None,
                      desired_width: float = None,
                      scale_factor_height: float = None,
                      scale_factor_width: float = None,
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
