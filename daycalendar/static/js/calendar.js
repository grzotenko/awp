$(document).ready(function(){
    getTime();
    theTimeHelper();
});
var editCellRoom = "";
var editCellTiming = [];
function theTimeHelper() {
    setInterval('getTime()',60000);
}
function getTime(){

    hour = moment().format("HH");
    dirtymin = moment().format("mm");

    if (Number(dirtymin) < 30){
        clearmin = 0;
    }
    else clearmin = 30;
    if (clearmin == "0"){
        clearmin = "00";
    }
    timelineMoves(hour, clearmin, dirtymin);
}
function timelineMoves(hour,clearmin, dirtymin)
{

    var marginTimeline = $("#"+hour+"-"+clearmin).position().top;
    marginTimeline+= (dirtymin - clearmin) * ($("#"+hour+"-"+clearmin).outerHeight()/30);
    $("#timeline").css("top", marginTimeline);
}
$('#dataCalendar').on('change',function () {
    var url = '/calendar/?date=' + $("#dataCalendar").val();
    $(location).attr('href',url);
})
$("body").on("click", ".cellBooking", function(e){
    var pk = $(this).attr("id").split("-")[1];
    var url = "/booking/edit/" + pk;
    $(location).attr('href',url);
});
$("body").on("click", ".cellEdit", function(e){
    $(this).addClass("cellFree");
    $(this).removeClass("cellEdit");
    var mas = $(this).attr("class").split(" ")[0].split("-")
    var str = mas[0] + "-" + mas[1];
    editCellTiming.splice(editCellTiming.indexOf(str), 1);
});
$("body").on("click", ".cellFree", function(e){
    $(this).addClass("cellEdit");
    $(this).removeClass("cellFree");
    var mas = $(this).attr("class").split(" ")[0].split("-")
    editCellRoom = mas[2];
    var str = mas[0] + "-" + mas[1];
    editCellTiming.push(str);
});
$("body").on("mousemove", ".cellFree", function(e){
    if (e.which === 1){
        $(this).addClass("cellEdit");
        $(this).removeClass("cellFree");
        var mas = $(this).attr("class").split(" ")[0].split("-");
        var str = mas[0] + "-" + mas[1];
        editCellRoom = mas[2];
        editCellTiming.push(str);
        console.log(editCellTiming);
    }
});
function compareNumeric(a, b) {
    a1 = a;
    b1 = b;
    var shift = "9-0";
    if ((Number(a.split("-")[0]) < Number(shift.split("-")[0])) || (Number(a.split("-")[0]) == Number(shift.split("-")[0]) &&  Number(a.split("-")[1]) < Number(shift.split("-")[1]))){
        x = Number(a.split("-")[0])+24;
        a1 = String(x) + "-" + a.split("-")[1];
    }
    if ((Number(b.split("-")[0]) < Number(shift.split("-")[0])) || (Number(b.split("-")[0]) == Number(shift.split("-")[0]) &&  Number(b.split("-")[1]) < Number(shift.split("-")[1]))){
        x = Number(b.split("-")[0])+24;
        b1 = String(x) + "-" + b.split("-")[1];
    }
    if (Number(a1.split("-")[0]) > Number(b1.split("-")[0])) return 1;
    if (Number(a1.split("-")[0]) < Number(b1.split("-")[0])) return -1;
    if (Number(a1.split("-")[1]) > Number(b1.split("-")[1])) return 1;
    if (Number(a1.split("-")[1]) < Number(b1.split("-")[1])) return -1;
}
function creaseData(a ,b){
    a1 = a;
    b1 = b;
    var shift = "9-0";
    if ((Number(a.split("-")[0]) < Number(shift.split("-")[0])) || (Number(a.split("-")[0]) == Number(shift.split("-")[0]) &&  Number(a.split("-")[1]) < Number(shift.split("-")[1]))){
        x = Number(a.split("-")[0])+24;
        a1 = String(x) + "-" + a.split("-")[1];
    }
    if ((Number(b.split("-")[0]) < Number(shift.split("-")[0])) || (Number(b.split("-")[0]) == Number(shift.split("-")[0]) &&  Number(b.split("-")[1]) < Number(shift.split("-")[1]))){
        x = Number(b.split("-")[0])+24;
        b1 = String(x) + "-" + b.split("-")[1];
    }
    var hours = Number(b1.split("-")[0]) - Number(a1.split("-")[0]);
    var minutes = Number(b1.split("-")[1]) - Number(a1.split("-")[1]);
    if (minutes < 0){
        hours--;
        minutes = 30;
    }
    return (String(hours) + "-" + String(minutes));
}
$("body").on("click", "#newbooking-Controller", function(e){
    e.preventDefault();
    editCellTiming.sort(compareNumeric);
    if (editCellTiming.length < 2){
        editCellTiming.push(editCellTiming[0]);
    }
    var lastTdClicked = editCellTiming[editCellTiming.length - 1].split("-");

    if (lastTdClicked[1] == "30"){
        lastTdClicked[1] = "0";
        lastTdClicked[0]++;
        strlastTdClicked = String(lastTdClicked[0]) + "-" + lastTdClicked[1];
    }
    else if (lastTdClicked[1] == "0"){
        lastTdClicked[1] = "30";
        strlastTdClicked = String(lastTdClicked[0]) + "-" + lastTdClicked[1];
    }
    editCellTiming[editCellTiming.length - 1] = strlastTdClicked;
    var duration = creaseData(editCellTiming[0], editCellTiming[editCellTiming.length - 1])
    var url = "/booking/new?from="+editCellTiming[0]+"&to="+editCellTiming[editCellTiming.length - 1]+"&duration="+duration+"&date="+$("#dataCalendar").val()+"&room="+editCellRoom;
    $(location).attr('href',url);
});