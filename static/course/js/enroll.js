$(".enroll").click(function (e) {
    var id = this.id; //$(this).attr('id');
    var href = $('.enroll').find('a').attr('href');
    e.preventDefault(); // don't follow the link

    $.ajax({
        url: href,
        data: {
          'enrollId': id
        },
        success: function(response){
          if(response.enrolled){
            $('#enrollbtn' + id).html("Enrolled");
          }
          else{
            $('#enrollbtn' + id).html("Enroll");
          }
        }
      })
});
