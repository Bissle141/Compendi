const cloudName = '{{cloudName}}'; 
const uploadPreset = 'Compendi_preset';

const addSectionBtn = document.getElementById("addSection");
const closeSectionBtn = document.getElementById("closeSectionCreation")
const firstImage = document.querySelector('.carousel-item')

if(firstImage){
    firstImage.classList.add('active')
}
if(addSectionBtn){
    addSectionBtn.addEventListener('click', addSectionClicked)
}
if(closeSectionBtn){
    closeSectionBtn.addEventListener('click', CloseSectionCreation)
}


function addSectionClicked () {
    let html = `<div id="NewSection" class="section-div mt-3"><div class="d-flex justify-content-end"><button id="closeSectionCreation" class="btn" type="button" style="background-color:transparent;"><span class="material-icons">close</span></button></div><form action="/file-edit/{{open_file.file_id}}/add-section" method="post" class="m-2"><div id="sectionName" class="d-flex flex-row justify-content-between form-group"><label for="sectionName" class="bebas mb-0" style="width: 200px; font-size:1.5rem;">Section Name</label><input type="text" class="form-control old" id="sectionName" name="sectionName" placeholder="Section Name"></div><div id="sectionBody" class="d-flex flex-column justify-content-between form-group"><label for="sectionBody" class="bebas" style="width: 200px; font-size:1.5rem;">Section Body</label><textarea name="sectionBody" id="sectionBody" rows="5" class="form-control old" placeholder="..."></textarea></div><div class="d-flex flex-row justify-content-end form-group mb-0"><button type="submit" class="btn bebas" style="background-color: #CBCD88; color:white;">Create</button></div></form></div>`    
    const sections_section = document.getElementById('newSections');
    sections_section.insertAdjacentHTML('afterbegin', html);
    document.getElementById("addSection").remove()

    document.getElementById("closeSectionCreation").addEventListener('click', CloseSectionCreation)
}

function CloseSectionCreation(){
    let html = `<button id='addSection' type="button" class="btn rounded mt-3" style="width:100%; background-color: #F5F2EA;"><span class="material-icons">add</span></button>`

    document.getElementById('NewSection').remove()
    
    document.getElementById('newSections').insertAdjacentHTML('afterend', html)

    document.getElementById("addSection").addEventListener('click', addSectionClicked)
}

function triggerSectionEdit(file_id, id){
    if (event.target.nodeName === 'SPAN') {
        editBtn = event.target.closest('#editSectionBtn')
    }
    else{
        editBtn = event.target
    }
    let header = editBtn.name
    let body = editBtn.value
    let html = `<form action="/${file_id}/section-edit/${id}" method="post" class="m-4"><div id="sectionName" class="d-flex flex-row justify-content-between form-group"><label for="sectionName" class="bebas mb-0" style="width: 200px; font-size:1.5rem;">Section Name</label><input type="text" class="form-control old" id="newSectionHeader" name="newSectionHeader" placeholder="Section Name" value="${header}"></div><div id="sectionBody" class="d-flex flex-column justify-content-between form-group"><label for="sectionBody" class="bebas" style="width: 200px; font-size:1.5rem;">Section Body</label><textarea name="sectionBody" id="sectionBody" rows="10" class="form-control old" placeholder="...">${body}</textarea></div><div class="d-flex flex-row justify-content-end form-group mb-0"><button type="submit" class="btn bebas" style="background-color: #CBCD88; color:white;">Save</button></div></form>`
    
    let card =document.getElementById(`${id}card`)
    while (card.firstChild) {
        card.removeChild(card.lastChild);
    }
    card.innerHTML = html
}


const myWidget = cloudinary.createUploadWidget({
    cloudName: cloudName,
    uploadPreset: uploadPreset,
    sources: ["url","camera","image_search","dropbox","instagram","shutterstock","getty","local","google_drive","facebook","istock","unsplash"],
    defaultSource: "url",
    multiple: false,

},
(error, result) => {
    if (!error && result && result.event === "success") {
    console.log("Done! Here is the image info: ", result.info);
    document
        .getElementById("uploadedimage")
        .setAttribute("src", result.info.secure_url);
    }
}
);

document.getElementById("upload_widget").addEventListener(
"click",
function () {
    myWidget.open();
},
false
);