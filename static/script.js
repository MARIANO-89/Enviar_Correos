// script.js
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
        },
        error: function(xhr, status, error) {
          // Mostrar error en caso de fallo
          alert("❌ Hubo un error: " + xhr.responseJSON.message);
        }
      });
    });
  });
  