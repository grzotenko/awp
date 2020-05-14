function matrixArray(rows,columns){
  var arr = new Array();
  for(var i=0; i<rows; i++){
    arr[i] = new Array();
    for(var j=0; j<columns; j++){
      arr[i][j] = null;//вместо i+j+1 пишем любой наполнитель. В простейшем случае - null
    }
  }
  return arr;
}


$('.schedule-shift').click(function () {
    if ($(this).hasClass('nice-time')) {
        $(this).removeClass('nice-time');
        $(this).addClass('bad-time');
    }
    else if ($(this).hasClass('bad-time')) {
        $(this).removeClass('bad-time');
    }
    else {
        $(this).addClass('nice-time');
    }
})
$("body").on("dblclick", ".my-shift", function(e){
    if ($(this).hasClass('not-wanted')) {
        $(this).removeClass('not-wanted')
    }
    else{
        $(this).toggleClass( "not-wanted" );
    }
});
$("body").on("dblclick", ".vacanted-shift", function(e){
    if ($(this).hasClass('vacanted-shift-change')) {
        $(this).removeClass('vacanted-shift-change')
        $(this).toggleClass("vacanted-shift");
    }
    else{
        $(this).removeClass('vacanted-shift');
        $(this).toggleClass("vacanted-shift-change");
    }
});
$("body").on("dblclick", ".vacanted-shift-change", function(e){
    if ($(this).hasClass('vacanted-shift-change')) {
        $(this).removeClass('vacanted-shift-change')
        $(this).toggleClass("vacanted-shift");
    }
    else{
        $(this).removeClass('vacanted-shift');
        $(this).toggleClass("vacanted-shift-change");
    }
});
$('#saveprefs-Controller').click(function(e){
    var dict = "";
    var url = "/management/saveprefs/";
    $('.schedule-shift').each(function(){
        time = $(this).parent().attr('class');
        list = $(this).attr('class').split(' ');
        day = list[1];
        if ($(this).hasClass('nice-time')){
            dict+= '+';
        }
        else if($(this).hasClass('bad-time')){
            dict+= '-';
        }
        else{
            dict+= '=';
        }
        dict+=";";
    })
    workWithShifts(url, dict);
//    e.preventDefault();
})
$('#givevacant-Controller').click(function(e){
    var dict = "";
    var url = "/management/givevacant/";
    $('.not-wanted').each(function(){
        dict += $(this).attr("id") + ","
    })
    workWithShifts(url, dict);
//    e.preventDefault();
})
$('#takevacant-Controller').click(function(e){
    var dict = "";
    var url = "/management/takevacant/";
    $('.vacanted-shift-change').each(function(){
        dict += $(this).attr("id") + ","
	})
    workWithShifts(url, dict);
//    e.preventDefault();
})
function workWithShifts(url, text){
    $.ajax({
        method: "POST",
        url: url,
        data: {
                'dict' : text,
        },
        dataType: 'json',
        success: function(data){
            if (data.key == "give"){
                alert("Выбранные вами смены стали возможными для выбора. Остальные пользователи будут уведомлены об этом.");
                $('.not-wanted').each(function(){
                    $(this).removeClass('not-wanted');
                    $(this).removeClass('my-shift');
                    $( this ).toggleClass("vacanted-shift");
                })
            }
            else if (data.key == "take"){
                alert("Вы успешно забрали данные смены!");
                counter = 0;
                $('.vacanted-shift-change').each(function(){
                    if ($(this).attr("id") == data.com[counter]){
                        $(this).removeClass('vacanted-shift-change');
                        $( this ).toggleClass( "my-shift" );
                        $(this).text(data.user);
                        $(this).css("background", data.color);
                        counter++;
                    }
                    else{
                        $(this).removeClass('vacanted-shift-change');
                        $(this).toggleClass("vacanted-shift");
                    }
                })
            }
            else {
                alert("Ваши изменения успешно внесены");
            }
        }
    })
}
$(document).ready(function(){
    $('.premiumTableContetntTr').each(function(){
        var type = ($(this).find('.premiumTableContetnt-typeTD').text());
        if (type == "Штраф") $(this).css({color: 'red'})
        else $(this).css({color: 'green'});
    });
    if(window.matchMedia('(max-width: 768px)').matches){
        var rows = matrixArray($("#currentPlanHeader th").length-1, 3);
        $("#currentPlanHeader th").remove();
        $headertr = '<th></th><th>Утро</th><th>Вечер</th><th>Вечер-2</th>';
        $("#currentPlanHeader").append($headertr);
        var i = 0;
        $("#currentPlan .morning-shift td").each(function(){
            rows[i][0] = $(this)[0];
            i++;
        })
        var i = 0;
        $("#currentPlan .evening-sfift td").each(function(){
            rows[i][1] = $(this)[0];
            i++;
        })
        var i = 0;
        $("#currentPlan .evening-2-shift td").each(function(){
            rows[i][2] = $(this)[0];
            i++;
        })
        $("#currentPlan tbody tr").remove();
        days = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]
        for (var i = 0; i < 7; i++){
            $("#currentPlan tbody").append('<tr class="'+i+'-shift"><th scope="row">'+days[i]+'</th></tr>');
            $("#currentPlan tbody ."+i+"-shift").append(rows[i][0]);
            $("#currentPlan tbody ."+i+"-shift").append(rows[i][1]);
            $("#currentPlan tbody ."+i+"-shift").append(rows[i][2]);
        }
        if ($("#futurePlan").length>0){
            var rows = matrixArray($("#futurePlanHeader th").length-1, 3);
            $("#futurePlanHeader th").remove();
            $headertr = '<th></th><th>Утро</th><th>Вечер</th><th>Вечер-2</th>';
            $("#futurePlanHeader").append($headertr);
            var i = 0;
            $("#futurePlan .morning-shift td").each(function(){
                rows[i][0] = $(this)[0];
                i++;
            })
            var i = 0;
            $("#futurePlan .evening-sfift td").each(function(){
                rows[i][1] = $(this)[0];
                i++;
            })
            var i = 0;
            $("#futurePlan .evening-2-shift td").each(function(){
                rows[i][2] = $(this)[0];
                i++;
            })
            $("#futurePlan tbody tr").remove();
            days = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]
            for (var i = 0; i < 7; i++){
                $("#futurePlan tbody").append('<tr class="'+i+'-shift"><th scope="row">'+days[i]+'</th></tr>');
                $("#futurePlan tbody ."+i+"-shift").append(rows[i][0]);
                $("#futurePlan tbody ."+i+"-shift").append(rows[i][1]);
                $("#futurePlan tbody ."+i+"-shift").append(rows[i][2]);
            }
        }
        else{
            var rows = matrixArray($("#teamChangeHeader th").length-1, 2);
            $("#teamChangeHeader th").remove();
            $headertr = '<th></th><th>Утро</th><th>Вечер</th>';
            $("#teamChangeHeader").append($headertr);
            var i = 0;
            $("#teamChange .morning-shift td").each(function(){
                rows[i][0] = $(this)[0];
                i++;
            })
            var i = 0;
            $("#teamChange .evening-shift td").each(function(){
                rows[i][1] = $(this)[0];
                i++;
            })
            $("#teamChange tbody tr").remove();
            days = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]
            for (var i = 0; i < 7; i++){
                $("#teamChange tbody").append('<tr class="'+i+'-shift"><th scope="row">'+days[i]+'</th></tr>');
                $("#teamChange tbody ."+i+"-shift").append(rows[i][0]);
                $("#teamChange tbody ."+i+"-shift").append(rows[i][1]);
            }
        }

    }
});