// Validación del formulario de creación
function validateForm() {
    const name = document.forms["createForm"]["name"].value;
    const lastName = document.forms["createForm"]["last-name"].value;
    const document = document.forms["createForm"]["document"].value;
    const address = document.forms["createForm"]["address"].value;
    const cellPhone = document.forms["createForm"]["cell-phone"].value;

    if (name == "" || lastName == "" || document == "" || address == "" || cellPhone == "") {
        alert("All fields must be filled out");
        return false;
    }

    if (document.length < 7 || document.length > 10) {
        alert("Document must be between 7 and 10 characters");
        return false;
    }

    const phonePattern = /^[0-9]{10}$/;
    if (!phonePattern.test(cellPhone)) {
        alert("Phone number must be exactly 10 digits and only numbers");
        return false;
    }

    return true; // Permite enviar el formulario
}

// Previsualización de la imagen
function previewImage(event) {
    var reader = new FileReader();
    reader.onload = function(){
        var output = document.getElementById('preview');
        output.src = reader.result;
        output.style.display = 'block';
    };
    reader.readAsDataURL(event.target.files[0]);
}

// Confirmación de eliminación
function confirmDelete() {
    return confirm("Are you sure you want to delete this record?");
}
