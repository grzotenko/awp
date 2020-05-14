$('#roomFilter').on('change',function () {
    $(".goldTr").each(function(){
        $(this).removeClass("goldTr");
    })
    var total = Number(0);
    $("#allSum").val(total);
    var $room = $('#roomFilter' + " :selected").text();
    var $roomVal = $('#roomFilter' + " :selected").val();
    if ($roomVal != 'hide') {
        $('#wd_id tr').each(function(){
            var r = ($(this).find('.room-td p').text());
            if($room == r){
                $(this).removeClass('hideByRoom');
                if (!($(this).hasClass("hideByCompany"))){
                    $(this).addClass('table-registry-tr');
                }
            }
            else{
                $(this).addClass('hideByRoom');
                $(this).removeClass('table-registry-tr');
            }
        })
    }
    else{
        $('#wd_id tr').each(function(){
            $(this).removeClass('hideByRoom');
            if (!($(this).hasClass("hideByCompany"))){
                $(this).addClass('table-registry-tr');
            }
        })
    }
});
$('#companyFilter').on('change',function () {
    $(".goldTr").each(function(){
        $(this).removeClass("goldTr");
        sum += Number($(this).find(".session-sum p").text());
    })
    var total = Number(0);
    $("#allSum").val(total);
    var $company = $('#companyFilter' + " :selected").text();
    var $companyVal = $('#companyFilter' + " :selected").val();
    if ($companyVal != 'hide') {
        $('#wd_id tr').each(function(){
            var c = ($(this).find('.company-td p').text());
            if($company == c){
                $(this).removeClass('hideByCompany');
                if (!($(this).hasClass("hideByRoom"))){
                    $(this).addClass('table-registry-tr');
                }
            }
            else{
                $(this).addClass('hideByCompany');
                $(this).removeClass('table-registry-tr');
            }
        })
    }
    else{
        $('#wd_id tr').each(function(){
            $(this).removeClass('hideByCompany');
            if (!($(this).hasClass("hideByRoom"))){
                $(this).addClass('table-registry-tr');
            }
        })
    }
});
$('#activeFilter').on('change',function () {
    var url = "/session?status=" + $('#activeFilter' + " :selected").val();
    $(location).attr('href',url);
});
$("body").on("dblclick", ".table-registry-tr", function(e){
    var url = $(location).prop('href') + "edit/" + $(this).attr("id");
    $(location).attr('href',url);
    e.preventDefault();
})
$("body").on("click", ".table-registry-tr", function(e){
    $allSum = $("#allSum");
    if (!($(this).hasClass("goldTr"))){
        $(this).addClass("goldTr");
        sum = Number($allSum.val());
        $allSum.val(sum + Number($(this).find(".session-sum p").text()));
    }
    else {
        $('#chooseAllinSes')[0].checked = false;
        $(this).removeClass("goldTr");
        sum = Number($allSum.val());
        $allSum.val(sum - Number($(this).find(".session-sum p").text()));
    }
})
$('#chooseAllinSes').click(function(){
    var sum = 0;
    if ($(this)[0].checked == true) {
        $("#wd_id .table-registry-tr").each(function(){
            if (!($(this).hasClass("goldTr"))){
                $(this).addClass("goldTr");
                sum += Number($(this).find(".session-sum p").text());
            }
        })
        console.log(sum);
        var total = Number($("#allSum").val()) + sum;
        $("#allSum").val(total);
    }
    else{
        $("#wd_id tr").each(function(){
            if ($(this).hasClass("goldTr")){
                $(this).removeClass("goldTr");
                sum += Number($(this).find(".session-sum p").text());
            }
        })
        var total = Number($("#allSum").val()) - sum;
        $("#allSum").val(total);
    }
})

//$("body").on("click", "#stopController", function(e){
//    var text = "";
//    $(".goldTr").each(function(){
//        text += $(this).attr("id") + ",";
//    })
//    var lastIndex = text.lastIndexOf(",");
//    text = text.substring(0 , lastIndex);
//    stopPayPrintDelete('/session/stop/', text);
//    //отмена действия по умолчанию для a
//    e.preventDefault();
//});

$("body").on("click", ".button-clicked", function(e){
    var text = "";
    var controller = $(this).attr("id").split("-")[0];
    var url = "/session/" + controller + "/";
    $(".goldTr").each(function(){
        text += $(this).attr("id") + ",";
    })
    var lastIndex = text.lastIndexOf(",");
    text = text.substring(0 , lastIndex);
    payInfo = $("#allSum").val() + "," + $("#cashIncome").val() + "," + $("#cardIncome").val()
    stopPayPrintDelete(url, text, payInfo);
    //отмена действия по умолчанию для a
    e.preventDefault();
});

function stopPayPrintDelete(url, text, payInfo){
    $.ajax({
        method: "POST",
        url: url,
        data: {
                'sessions' : text,
                'payInfo' : payInfo,
        },
        dataType: 'json',
        success: function(data){
             if (data.type == "stop"){
                var i = 0;
                $(".goldTr").each(function(){
                    $(this).find(".session-sum p").text(data.sessions[i]);
                    i++;
                })
                $("#allSum").val(data.allPrice);
             }
             else if (data.type == "delete" || data.type == "print"){
                location.reload();
             }
             else if (data.type == "pay"){
                if (data.info == "error"){
                    location.reload();
                }
                else{
                    var url = $(location).prop('href') + "payfinal/" + data.payment;
                    $(location).attr('href',url);
                }
             }
//             for (var i=0;i<data.sessions.length;i+=1){
//                $("#wd_id #" + data.sessions[i]).addClass("goldTr");
//            }
        }
    })
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
};
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});