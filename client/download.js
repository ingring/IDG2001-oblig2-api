async function downloadFile(){
    console.log('in download.js')
    let APIurl = "https://api-production-f028.up.railway.app/contacts/vcard"

    try {
        //fetch request for the API 
        const response = await fetch(APIurl, {
            method: 'GET',
            headers: {'Content-Type':'application/json'},
          })

        //retrieve the text from the response body
        const textData = await response.text()
        console.log(textData)

        // parse the text from the response body to json format
        const jsonData = JSON.parse(textData)

        //get the vcard data inside the message statement
        const message = jsonData.message

        //using "blob" for convert data to a blob object - this is for creating a URL for the file
        //also setting the file format to vcf
        const blob = new Blob([message], {type: "text/vcard"});

        //create a url for the file
        const fileUrl = URL.createObjectURL(blob)

        //create a new anchor element with the download URL
        const downloadLink = document.createElement('a');

        //making a href for the fileURL and setting a "download" and a "click" - this is so the file will 
        //be downloaded as contact.vcf and is downloaded to the computer.
        downloadLink.href = fileUrl
        downloadLink.download = 'contact.vcf'
        downloadLink.click();
        URL.revokeObjectURL(downloadLink.href);

    } catch (error) {
        console.error('Error:', error);
    }
}
