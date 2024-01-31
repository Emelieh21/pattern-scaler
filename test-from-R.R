# Make post request with png file
library(httr)

setwd(dirname(rstudioapi::getSourceEditorContext()$path))

# URL of your FastAPI endpoint
url <- "http://localhost:8001/scale_pattern?desired_height=42&line_width=2"

# Path to the PNG file
file_path <- "src/test-inputs/sweater-bottom.png"

# Create a POST request with the PNG file
response <- POST(
  url,
  body = list(file = upload_file(file_path, "image/png")),
  encode = "multipart"
)

print(response$headers$`x-original-width`)
print(response$headers$`x-original-height`)
print(response$headers$`x-new-width`)
print(response$headers$`x-new-height`)

# Check if the request was successful (status code 200)
if (http_status(response)$category == "Success") {
  # Get the content of the response
  pdf_content <- content(response, as = "raw")
  # Specify the path where you want to save the PDF
  pdf_path <- "result.pdf"
  
  # Write the PDF content to the file
  writeBin(pdf_content, pdf_path)
  
  cat("PDF saved successfully at:", pdf_path, "\n")
} else {
  cat("Failed to retrieve the PDF. HTTP status code:", http_status(response)$status_code, "\n")
}

