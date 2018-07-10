$(document).ready( function() {
    /* Executa a requisição quando o campo CEP perder o foco */
    $('#cepp').blur(function(){
            /* Configura a requisição AJAX */
            $.ajax({
                 url : '/cep', /* URL que será chamada */ 
                 type : 'POST', /* Tipo da requisição */ 
                 data: 'cep=' + $('#exampleFormControlSelect2').val(), /* dado que será enviado via POST */
                 dataType: 'json', /* Tipo de transmissão */
                 success: function(data){
                     if(data.sucesso == 1){
                         $('#exampleFormControlSelect3').val(data.rua);
                         $('#exampleFormControlSelect4').val(data.bairro);     
  
                         $('#number').focus();
                     }
                 }
            });   
    return false;    
    })
 });