//构建XMLHttpRequest对象
function createXMLHttpRequest(){
    var xmlHttp;
    if (window.XMLHttpRequest){
        xmlHttp = new XMLHttpRequest();
        if (xmlHttp.overrideMimeType){
            xmlHttp.overrideMimeType('text/xml');
        }
    }
    else if (window.ActiveXobject){
        try{
            xmlHttp = new ActiveXObject("Msxml2.XMLHTTP");
        }
        catch(e){
            try{
                xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
            }
            catch(e){}
        }
    }
    return xmlHttp;
}

//回调函数
var html_data = "";
var sql_data = {};
var callback = function (){
    sql_data = JSON.parse(request.responseText);
    if (typeof(sql_data[0]) !== "undefined"){
        html_data = "<table class='head-table'>";
		html_data+= "<tr><th class='t1'>Username</th>";
		html_data+= "<th class='t2'>Pingyin</th>";
		html_data+= "<th class='t3'>Email</th>";
		html_data+= "<th class='t4'>Office</th>";
        if (sql_data['status']){
		    html_data+= "<th class='t5'>Mobile</th>";
        }
		html_data+= "<th class='t6'>Team</th></tr>";
		html_data+= "<tr><td class='t7'></td></tr>";
        for (count in sql_data){
            if ('status' != count){
                html_data+= "<tr>";
                html_data+= "<td>" + sql_data[count]['username'] + "</td>";
                html_data+= "<td>" + sql_data[count]['pingyin'] + "</td>";
                html_data+= "<td>" + sql_data[count]['email'] + "</td>";
                html_data+= "<td>" + sql_data[count]['office'] + "</td>";
                if (sql_data['status']){
                    html_data+= "<td>" + sql_data[count]['mobile'] + "</td>";
                }
                html_data+= "<td>" + sql_data[count]['team'] + "</td>";
                html_data+= "</tr>";
            }
        }
        html_data+= "</table>";
    }
}

function search_user_info(data){
    request = createXMLHttpRequest();
    var url = "/staffInfo/search";
    request.open("POST", url); 
    request.onreadystatechange = function(){
        if(request.readyState === 4 && callback){
            callback();
        }
    };
    request.setRequestHeader("Content-Type", "application/json");
    request.send(JSON.stringify(data));
}

var form = {};
var flag = false;
setValue = function (){
    if (form['username'] != $('input[id=username]').val()){
        form['username'] = $('input[id=username]').val();
        flag = true;
    }
    if (form['email'] != $('input[id=email]').val()){
        form['email'] = $('input[id=email]').val();
        flag = true;
    }
    if (form['team'] != $('input[id=team]').val()){
        form['team'] = $('input[id=team]').val();
        flag = true;
    }
    if (form['extension'] != $('input[id=extension]').val()){
        form['extension'] = $('input[id=extension]').val();
        flag = true;
    }
    if (flag){
        search_user_info(form);
        flag = false;
    }
    $(function(){
            $("div[id^=search-data]").html(html_data);
            $("div[id^=search-data]").css("margin", "0.5em auto");
            $("div[id^=search-data]").css("text-align", "center");
            if (sql_data['status']){
                $("div[id^=search-data]").css("width", "51em");
            }
            else{
                $("div[id^=search-data]").css("width", "45em");
            }
            });
}

var clear_flag = false;
function onFocus(object){
	object.value = '';
        if (!clear_flag){
		$('input[id=username]').val('');
		$('input[id=email]').val('');
		$('input[id=team]').val('');
		$('input[id=extension]').val('');
		clear_flag = true;
	}

	object.style.color = "black";
    //定时器
    timerID = setInterval("setValue()", 200);
}

function onBlur(object){
    clearInterval(timerID);
}


