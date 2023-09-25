from simple_salesforce import Salesforce
import os
import requests

def fetch_and_send_pdf():
    # Salesforce credentials
    username = "your_username"
    password = "your_password"
    security_token = "your_security_token"
    domain = "login"

    # Initialize Salesforce client
    sf = Salesforce(username=username, password=password, security_token=security_token, domain=domain)

    # Fetch PDF ContentVersions
    pdf_content_versions = sf.query("SELECT Id, Title, VersionData FROM ContentVersion WHERE FileExtension = 'pdf'")

    folder_path = '/your-folder-path/pdf-download'
    
    # Download and save PDF files
    for record in pdf_content_versions['records']:
        if not os.path.exists(os.path.join(folder_path, record['Id'])):
            os.mkdir(os.path.join(folder_path, record['Id']))


        pdf_data = sf.ContentVersion.get(record['Id'])
        file_name = record['Title'] + '.pdf'
        

        # Save PDF file to a local folder
        with open(os.path.join(folder_path, record['Id'], file_name), 'wb') as pdf_file:
            pdf_file.write(pdf_data['VersionData'])

    send_pdf_to_soap(pdf_content_versions)


def send_pdf_to_soap(pdf_content_versions):
    # Define SOAP API endpoint and headers
    soap_api_url = 'https://example.com/soap-endpoint'
    headers = {'Content-Type': 'text/xml;charset=UTF-8'}

    # Iterate through saved PDFs and send them to the SOAP API
    for record in pdf_content_versions['records']:
        file_name = record['Title'] + '.pdf'
        
        # Open and read the PDF file
        with open(file_name, 'rb') as pdf_file:
            pdf_content = pdf_file.read()
        
        # Construct SOAP request payload (adjust as per your API)
        soap_payload = f"""
        <Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
            <Body>
                <UploadPDF>
                    <FileName>{file_name}</FileName>
                    <PDFContent>{pdf_content}</PDFContent>
                </UploadPDF>
            </Body>
        </Envelope>
        """
        
        # Send the SOAP request
        response = requests.post(soap_api_url, data=soap_payload, headers=headers)
        
        # Process the SOAP API response as needed
        print(f"Uploaded {file_name} - Response: {response.text}")

