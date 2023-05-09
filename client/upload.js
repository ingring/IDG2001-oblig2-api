function uploadFile() {
  let APIurl = "https://api-production-f028.up.railway.app/contacts"

  // get the file
  let fileInput = document.getElementById('file');
  let file = fileInput.files[0];

  // doble checks if the file is a .vcf file
  if (!file.name.endsWith('.vcf') || !['text/vcard', 'text/x-vcard', 'application/vcard', 'application/x-vcard'].includes(file.type)) {
    console.error('Invalid file format')
    return
  }

  // read the file 
  let reader = new FileReader()
  reader.readAsText(file, 'UTF-8')

  // when the file is completly loaded, it will fetch the data from the file, and send it to the backend
  reader.onload = function(){
    let vcardText = reader.result
    let dataObject = {message:vcardText}
    let data = JSON.stringify(dataObject)
    console.log(data);
    fetch(APIurl, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: data
    })
    .then(res => {
      console.log(res);
      return res.json()
    })
    .then(data => console.log(data))
    .catch(error => {
      console.error(error);
    })
  }
}
