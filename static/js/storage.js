$('#warehouseIn-category').on('change',function () {WarehouseFilter("cat","#warehouseIn-category","#warehouseIn-subcategory","#warehouseIn-good")})
$('#warehouseIn-subcategory').on('change',function () {WarehouseFilter("subcat","#warehouseIn-category","#warehouseIn-subcategory","#warehouseIn-good")})

$('#warehouseOut-category').on('change',function () {WarehouseFilter("cat","#warehouseOut-category","#warehouseOut-subcategory","#warehouseOut-good"); killSelect('#warehouseOut-volume', '-- Объем --')})
$('#warehouseOut-subcategory').on('change',function () {WarehouseFilter("subcat","#warehouseOut-category","#warehouseOut-subcategory","#warehouseOut-good"); killSelect('#warehouseOut-volume', '-- Объем --')})

$('#warehouse-selects-category').on('change',function () {WarehouseFilter("cat","#warehouse-selects-category","#warehouse-selects-subcategory","#warehouse-selects-good", true)})
$('#warehouse-selects-subcategory').on('change',function () {WarehouseFilter("subcat","#warehouse-selects-category","#warehouse-selects-subcategory","#warehouse-selects-good", true)})
$('#warehouse-selects-good').on('change',function () {WarehouseFilter("good","#warehouse-selects-category","#warehouse-selects-subcategory","#warehouse-selects-good", true)})
$('#period-selects-category').on('change',function () {WarehouseFilter("cat","#period-selects-category","#period-selects-subcategory","#period-selects-good", true, ".period-table-tr", ".period-table-good-td")})
$('#period-selects-subcategory').on('change',function () {WarehouseFilter("subcat","#period-selects-category","#period-selects-subcategory","#period-selects-good", true, ".period-table-tr", ".period-table-good-td")})
$('#period-selects-good').on('change',function () {WarehouseFilter("good","#period-selects-category","#period-selects-subcategory","#period-selects-good", true, ".period-table-tr", ".period-table-good-td")})
$('#warehouseOut-good').on('change',function(){
    $volume = $('#warehouseOut-volume');
    if ($("#warehouseOut-good" + ' :selected').val() != 'hide') {
        $($volume).find('option').remove();
        $.ajax({
            method: "POST",
            url:'/warehouse/VolumeFilter/',
            data: {
                'good': $("#warehouseOut-good" + " :selected").val(),
            },
            dataType: 'json',
            success: function(data){
                selectReDraw($volume, data.aV, '-- Объем --')
            }
        })
    }
    else {
        killSelect($volume, '-- Объем --');
    }
})
$('#warehouseOut-volume').on('change',function(){
    $volume = $("#warehouseOut-volume" + ' :selected').val();
    if ($volume != 'hide') {
        $good = $("#warehouseOut-good" + ' :selected').val();
        $('#outModalAmount').prop('disabled', false);
        $.ajax({
            method: "POST",
            url:'/warehouse/AmountFilter/',
            data: {
                'good': $good,
                'volume' : $volume,
            },
            dataType: 'json',
            success: function(data){
                $('#outModalAmount').prop('max', data.a);
                $('#outModalAmount').val('');
            }
        })
    }
});
function WarehouseFilter(type, catId, subcatId, goodId, cons = false, ttr = '.table-consumables-tr', ttd = '.table-consumables-good-td'){
    $cat = $(catId + " :selected").val();
    if (type =='cat'){
        $subcat = 'hide';
        $good = 'hide';
    }
    else{
        $subcat = $(subcatId + " :selected").val();
    }

     $.ajax({
            method : "POST" ,
            url : '/warehouse/WarehouseFilter/',
            data: {
                'ThisCat' :  $cat,
                'ThisSubcat' : $subcat,
            },
             dataType: 'json',
             success: function(data){
                if(type != "good"){
                    if (cons == true) {
                        $('body').find(ttr).each(function(){
                        var t = ($(this).find(ttd).text());
                        if($.inArray(t, data.aG) != -1){
                            console.log(this);
                            $(this).css({display: 'table-row'});
                        }
                        else{
                            $(this).css({display: 'none'});
                        }
                    })
                    }

                    if (type == "cat") {
                        selectReDraw(subcatId, data.aS, '-- Все подкатегории --');
                    }
                    selectReDraw(goodId, data.aG, '-- Все товары --');
                }
                else{
                    var tG = $(goodId + " :selected").val();
                    if (tG != "hide"){
                        $('body').find(ttr).each(function(){
                            var t = ($(this).find(ttd).text());
                            if(tG == t){
                                $(this).css({display: 'table-row'});
                            }
                            else{
                                $(this).css({display: 'none'});
                            }
                        })
                    }
                    else{
                          $('body').find(ttr).each(function(){
                        var t = ($(this).find(ttd).text());
                        if($.inArray(t, data.aG) != -1){
                            $(this).css({display: 'table-row'});
                        }
                        else{
                            $(this).css({display: 'none'});
                        }
                    })
                    }
                }

             }})
};

function selectReDraw(selector, items, text){
    $(selector).find('option').remove();
    $(selector).append($('<option>', {
        value: 'hide',
        text: text
    }));
    $.each(items, function (i, item) {
        $(selector).append($('<option>', {
            value: item,
            text : item
        }));
    });
}
function killSelect(select, text){
    $(select).find('option').remove();
    $(select).append($('<option>', {
        value: 'hide',
        text: text
    }));
    $('#outModalAmount').prop('disabled', true);
    $('#outModalAmount').val('');
}
$('#wrhsInamount').on('change keyup',function(){
	amount = $('#wrhsInamount').val();
	price  = $('#wrhsInprice').val();
	cost   = $('#wrhsIncost').val();
	if (amount != 0 && amount != '') {
		if (price != 0 && price != '') {
			$('#wrhsIncost').val(amount * price)
		}
		else if (cost != 0 && cost != '') {
			$('#wrhsInprice').val(cost / amount)
		}
	}
});
$('#wrhsInprice').on('change keyup',function(){
	amount = $('#wrhsInamount').val();
	price  = $('#wrhsInprice').val();
	cost   = $('#wrhsIncost').val();
	if (amount != 0 && amount != '') {
		$('#wrhsIncost').val(amount * price)
	}
});
$('#wrhsIncost').on('change keyup',function(){
	amount = $('#wrhsInamount').val();
	price  = $('#wrhsInprice').val();
	cost   = $('#wrhsIncost').val();
	if (amount != 0 && amount != '') {
		$('#wrhsInprice').val(cost / amount)
	}
});
$(document).ready(function(){
	var tabs = $('#warehouseTabsMenu');
	var selector = $('#warehouseTabsMenu').find('a').length;
	var activeItem = tabs.find('.active');
	var activeWidth = activeItem.innerWidth();
	$(".warehouseSelector").css({
	  "left": activeItem.position.left + "px", 
	  "width": activeWidth + "px"
});

	$('.table-storage-content-tr').each(function(){
	   var type = ($(this).find('.storage_type').text());
        if (type == "Приход") $(this).css({color: 'green'})
            else $(this).css({color: 'red'});
    });
    $(".warehouseTabsMenu_tab").click(function(){ 
		if (!$(this).hasClass("active")) { 
		var i = $(this).index(); 
		$(".warehouseTabsMenu_tab.active").removeClass("active"); 
		$("#warehouseTabs .active").hide().removeClass("active"); 
		$("#warehouse-tools .active").hide().removeClass("active"); 
		$(this).addClass("active"); 
		 var activeWidth = $(this).innerWidth();
  		 var itemPos = $(this).position();
		 $(".warehouseSelector").css({
		    "left":itemPos.left + "px", 
		    "width": activeWidth + "px"});
		$($("#warehouseTabs").children(".storageTab")[i-1]).fadeIn(1000).addClass("active");
		$($("#warehouse-tools").children(".warehouse-tool")[i-1]).fadeIn(1000).addClass("active");
		}
});

$('#wthsModalInBtn').click(function(){
	var good = $('#warehouseIn-good :selected').val();
	var volume = $('#wrhsInvolume').val();
	var amount = $('#wrhsInamount').val();
	var cost = $('#wrhsIncost').val();
	if (good == 'hide' || volume.length == 0 || amount.length == 0 || cost.length == 0) {
		alert("Выберите товар и заполните объём, количество упаковок и общую стоимость!");
	}
	else{
		$.ajax({
			method: "POST",
			url: "/warehouse/WrhsIn",
			data: {
				'good' : good,
				'volume' : volume,
				'amount' : amount,
				'cost' : cost,

			},
			dataType: 'json',
	        success: function(data){
	        	alert('Успешно! Товар: ' + data.g + ' на складе ' + data.a + ' упаковок объемом ' + data.v );
	        	window.location.reload();
	        }
		})
	}
	
})
$('#wthsModalOutBtn').click(function(){
	var $good = $('#warehouseOut-good :selected').val();
	var $volume = $('#warehouseOut-volume :selected').val();
	var $amount = $('#outModalAmount');
	var $comment = '';	
	if ($good == 'hide' || $volume == 'hide' || $amount.length == 0 || $amount.val() == 0){
		alert("Выберите товар и заполните объём и количество упаковок!");
	}
	else {
		$comment += $('#outModalComment').val();
		$.ajax({
			method: "POST",
			url: "/warehouse/WrhsOut/",
			data: {
				'good' : $good,
				'volume' : $volume,
				'amount' : $amount.val(),
				'comment' : $comment,

			},
			dataType: 'json',
			success: function(data){
	        	alert('Успешно! Товар: ' + data.g + ' на складе ' + data.a + ' упаковок объемом ' + data.v );
	        	window.location.reload();
	        }
		})
	}
})
$('#outModalAmount').on('change keyup',function(){
        v = parseInt($(this).val());
        min = parseInt($(this).attr('min'));
        max = parseInt($(this).attr('max'));
        var sanitized = $(this).val().replace(/[^0-9]/g, '');
  		$(this).val(sanitized);
        if (v < min){
            $(this).val(min);
        } else if (v > max){
            $(this).val(max);
        }
    })

});


$('#periodBtn').click(function(){
	start = $('#period_start').val();
	end = $('#period_end').val();
	sD = new Date(start);
	eD = new Date(end);
	delta = eD.getTime() - sD.getTime();
	if (delta < 0){
		alert('Неправильно введенные даты!')
	}
	else{
		$.ajax({
			method: "POST",
			url: "/warehouse/wrhsPeriod/",
			data: {
				'start' : start,
				'end' : end,
			},
			dataType: 'json',
			success: function(data){
	        	table = '';
	        	for (i = 0; i < data.lfP.length; i++){
	        		table = table + '<tr class="period-table-tr">' + '<td>' + data.lfP[i].cat + '</td>' +'<td>' + data.lfP[i].sub + '</td>'+'<td class="period-table-good-td">' + data.lfP[i].good + '</td>'+'<td>' + data.lfP[i].units + '</td>'+ '<td>' + data.lfP[i].cost + '</td>' +'</tr>';
	        	}
	        	table += '<tr><td></td><td></td><td></td><td></td><td class="period-total-sum">Общая сумма: ' + data.ts +'</td></tr>'
	        	$('#period-table tbody').html(table);
	        }
		})
	}
	
	
})
