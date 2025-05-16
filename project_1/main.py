from fastapi import FastAPI, UploadFile, File
import pandas as pd
from fastapi.responses import HTMLResponse

app = FastAPI("app.py")
path = r"C:\Users\TARANI\OneDrive\Desktop\LPR\veh.csv"
@app.post(path)
async def upload_file(file: UploadFile = File(...)):
    # Read the uploaded Excel file into a DataFrame
    df = pd.read_excel(file.file)

    # Convert DataFrame to HTML table
    html_table = df.to_html(classes='table table-striped', index=False)

    return HTMLResponse(content=html_table)

@app.get("/")
async def main():
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>License Plate Recognition - Upload Excel File</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <style>
            body {
                background-color: #f8f9fa;
            }
            .container {
                margin-top: 50px;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                background-color: #ffffff;
            }
            h2 {
                color: #343a40;
            }
            .btn-primary {
                background-color: #007bff;
                border-color: #007bff;
            }
            .btn-primary:hover {
                background-color: #0056b3;
                border-color: #0056b3;
            }
            table {
                margin-top: 20px;
                width: 100%;
            }
            th, td {
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2 class="text-center">Upload an Excel File</h2>
            <form action="/uploadfile/" method="post" enctype="multipart/form-data" class="text-center">
                <input type="file" name="file" accept=".xlsx, .xls" required class="form-control-file mb-3">
                <button type="submit" class="btn btn-primary">Upload</button>
            </form>

            <!-- This section will be filled with the HTML table after file upload -->
            <div id="result"></div>
        </div>

        <script>
            // Function to handle displaying the result
            async function displayResult(data) {
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = data; // Insert the HTML table
            }

            // Check if there is any result to display
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.has('result')) {
                const result = urlParams.get('result');
                displayResult(result);
            }
        </script>
    </body>
    </html>
    """)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)