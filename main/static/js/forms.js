$("#id_servicesChange option").each(function(){
    $(this).prop('hidden',true);
})

$("body").on("click", "#id_servicesChange option", function(e){
        var ur = $(this)[0];
        $("#id_servicesChange option[value='"+ur.value+"']").prop('hidden',true);
        $("#id_servicesChange option[value='"+ur.value+"']").prop('selected',false);
        $("#id_servicesAll option[value='"+ur.value+"']").prop('hidden',false);
        $("#id_servicesChange option:not(:hidden)").each(function(){
            var ur = $(this)[0];
            $("#id_servicesChange [value='"+ ur.value +"']").prop("selected", true);
        })
})

$("body").on("change", "#id_servicesAll", function(e){
    $("#id_servicesAll option:selected").each(function(){
        var ur = $(this)[0];
        $("#id_servicesAll option[value='"+ur.value+"']").prop('hidden',true);
        $("#id_servicesAll [value='"+ ur.value +"']").prop("selected", false);

        $("#id_servicesChange [value='"+ ur.value +"']").prop("hidden", false);
        $("#id_servicesChange [value='"+ ur.value +"']").prop("selected", true);
    })
})

$("#id_includesChange option").each(function(){
    $(this).prop('hidden',true);
})

$("body").on("click", "#id_includesChange option", function(e){
        var ur = $(this)[0];
        $("#id_includesChange option[value='"+ur.value+"']").prop('hidden',true);
        $("#id_includesChange option[value='"+ur.value+"']").prop('selected',false);
        $("#id_includesAll option[value='"+ur.value+"']").prop('hidden',false);
        $("#id_includesChange option:not(:hidden)").each(function(){
            var ur = $(this)[0];
            $("#id_includesChange [value='"+ ur.value +"']").prop("selected", true);
        })
})

$("body").on("change", "#id_includesAll", function(e){
    $("#id_includesAll option:selected").each(function(){
        var ur = $(this)[0];
        $("#id_includesAll option[value='"+ur.value+"']").prop('hidden',true);
        $("#id_includesAll [value='"+ ur.value +"']").prop("selected", false);

        $("#id_includesChange [value='"+ ur.value +"']").prop("hidden", false);
        $("#id_includesChange [value='"+ ur.value +"']").prop("selected", true);
    })
})

$('#id_tariff').on('change',function () {
    var value = $(this).val();
    var url = "/session/tariff/" + value + "/";
    changeTariffDiscount(url);
});

$('#id_discount').on('change',function () {
    var value = $(this).val();
    var url = "/session/discount/" + value + "/";
    changeTariffDiscount(url);
});

function changeTariffDiscount(url){
    $.ajax({
        method: "POST",
        url: url,
        data: {
        },
        dataType: 'json',
        success: function(data){
            if (data.type == "tariffs"){
                $('#id_count').attr('min', data.minimum);
                $('#id_count').attr('value', data.minimum);
//                $('#id_discount option:not(:first)').remove();
//                for (var i = 0;i < data.count;i++){
//                    $('#id_discount').append('<option value="'+data.discounts[i].id+'">'+data.discounts[i].name+'</option>');
//                }
                $('#id_discount option:not(:first)').attr("hidden",true);
                for (var i = 0;i < data.count;i++){
                    $("#id_discount option[value='"+data.discounts[i].id+"']").prop('hidden',false);
                }
             }
             else if (data.type == "discounts"){
                $('#id_count').attr('min', data.minimum);
                $('#id_count').attr('max', data.maximum);
                $('#id_count').attr('value', data.minimum);
             }
        }
    })
}


//BOOKINGS
$('#id_duration').on('change',function () {
    $("#id_time_end").val(changeTime($("#id_time_start").val(), $("#id_duration").val()));
})
$('#id_time_end').on('change',function () {
    $("#id_duration").val(creaseData($("#id_time_start").val(), $("#id_time_end").val(), $("#id_shift").val()));
})
$('#id_time_start').on('change',function () {
    $("#id_duration").val(creaseData($("#id_time_start").val(), $("#id_time_end").val(), $("#id_shift").val()));
})
function creaseData(a ,b, shift){
    a1 = a;
    b1 = b;
    if ((Number(a.split(":")[0]) < Number(shift.split(":")[0])) || (Number(a.split(":")[0]) == Number(shift.split(":")[0]) &&  Number(a.split(":")[1]) < Number(shift.split(":")[1]))){
        x = Number(a.split(":")[0])+24;
        a1 = String(x) + ":" + a.split(":")[1];
    }
    if ((Number(b.split(":")[0]) < Number(shift.split(":")[0])) || (Number(b.split(":")[0]) == Number(shift.split(":")[0]) &&  Number(b.split(":")[1]) < Number(shift.split(":")[1]))){
        x = Number(b.split(":")[0])+24;
        b1 = String(x) + ":" + b.split(":")[1];
    }
    var hours = Number(b1.split(":")[0]) - Number(a1.split(":")[0]);
    var minutes = Number(b1.split(":")[1]) - Number(a1.split(":")[1]);
    if (minutes < 0){
        hours--;
        minutes = 30;
    }
    if (hours<10){
        var hoursStr = "0" + String(hours);
    }
    else {
        var hoursStr = String(hours);
    }
    if (minutes==0){
        minutes = "0" + String(minutes);
    }
    return (hoursStr + ":" + String(minutes));
}
function changeTime(a, b){
    var hours = Number(a.split(":")[0]) + Number(b.split(":")[0]);
    var minutes = Number(a.split(":")[1]) + Number(b.split(":")[1]);
    if (minutes == 60) {
        var minutesStr = "00";
        hours++;
    }
    else if (minutes == 30){
        var minutesStr = "30";
    }
    else{
        var minutesStr = "00";
    }
    if (hours>=24){
        hours-=24;
    }
    if (hours<10){
        var hoursStr = "0" + String(hours);
    }
    else{
        var hoursStr = String(hours);
    }
    return (hoursStr+":"+minutesStr);
}




//READY
$(document).ready(function(){
    $('#id_discount option:not(:first)').attr("hidden",true);

});