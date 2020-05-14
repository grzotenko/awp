$("body").on("dblclick", ".table-booking-tr", function(e){
    var url = $(location).prop('href') + "edit/" + $(this).attr("id");
    $(location).attr('href',url);
    e.preventDefault();
})