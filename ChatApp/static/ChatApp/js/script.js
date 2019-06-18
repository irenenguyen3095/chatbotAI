$(document).ready(function() {
        var product= $(".classform")
        product.submit(function(event){
          event.preventDefault();
          var thisform= $(this)
          var actionEndpoint=thisform.attr("action");
          var httpMethod=thisform.attr("method");
          var formData= thisform.serialize();
          var data= { 'msgbox' : $('#chat-msg').val() }
          console.log(thisform.attr("action"), thisform.attr("method"), formData, data)

          $.ajax({
              url:actionEndpoint,
              method:httpMethod,
              data:{ 'msgbox' : $('#chat-msg').val() },
              //'type':'POST',
             // 'data':{ 'msgbox' : $('#chat-msg').val() },
              //data : { 'msgbox' : $('#chat-msg').val() },
              success: function(response){
                console.log("success")
                console.log(response)
                $('#msg-list').append('<li class="text-left list-group-item list-group-item-primary">' + response.rep + '</li>');
                $('#msg-list').append('<li class="text-right list-group-item">' + response.msg + '</li>');
                $('#chat-msg').val('');
                $('.choose').val("response.rep");
              },
              error: function(errordata){
                console.log("Error", errordata)
              }
          })
        })
    });
