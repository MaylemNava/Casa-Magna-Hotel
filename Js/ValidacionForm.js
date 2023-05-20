// Obtenemos valores de los campos
var nombre = document.getElementById('nombre').value;
var celular = document.getElementById('celular').value;
var correo = document.getElementById('correo').value;
var mensaje = document.getElementById('mensaje').value;

// Validacion de los campos que no esten vacios (Con required se hace en html)

if (nombre.trim() === '' || celular.trim() === '' || correo.trim() === '' || mensaje.trim() === ''){
    alert("Por favor, completa todos los campos")
    return;
}