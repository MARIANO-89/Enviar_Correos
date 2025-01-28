$(document).ready(function() {
    // Función para manejar el envío de correos
    $('#form-enviar').on('submit', function(event) {
      event.preventDefault();
      var formData = new FormData(this);
  
      $.ajax({
        url: '/enviar', 
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
          // Mostrar el pop-up de éxito
          alert("🚀 Enviado con éxito 🚀");
  
          // Resetear el formulario
          $('#form-enviar')[0].reset();
  
          // Eliminar datos sensibles de las variables de formulario
          $('#correo_emisor').val('');
          $('#contrasena').val('');
        },
        error: function(xhr, status, error) {
          // Mostrar error en caso de fallo
          if (xhr.responseJSON && xhr.responseJSON.message) {
            alert("❌ Hubo un error: " + xhr.responseJSON.message);
          } else {
            alert("❌ Hubo un error inesperado.");
          }
        }
      });
    });
  });
  