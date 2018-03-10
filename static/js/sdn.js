STATIC_PATH = "/static/";
QUERY_PATH = "/api";

function fixNum(num) {
	return Number(num && num != Infinity ? num.toFixed(2) : 0);
}

function fixInt(num) {
	if(num>0&&num<1){
		return num.toFixed(2);
	}
	return Number(num && num != Infinity ? num.toFixed(0) : 0);
}

function getUrlRequest() {
	var url = location.search;
	var theRequest = new Object();
	if(url.indexOf("?") != -1) {
		var str = url.substr(1);
		if(str.indexOf("&") != -1) {
			strs = str.split("&");
			for(var i = 0; i < strs.length; i++) {
				theRequest[strs[i].split("=")[0]] = decodeURI(strs[i].split("=")[1]);
			}
		} else {
			var key = str.substring(0, str.indexOf("="));
			var value = str.substr(str.indexOf("=") + 1);
			theRequest[key] = decodeURI(value);
		}
	}
	return theRequest;
}

function sort(obj, index1, index2, rev) { //rev 正逆序
	function sortByIndex(a, b) { //这个对象中需要被排序的元素  a和b的排位顺序正确时返回a,b  否则返回b,a。
		if(!rev) { //若从高到低
			if(a[index1] == b[index1] && index2) { // 第一个索引值相等时比较第二个索引值
				return ($.type(a[index2])=="number"||$.type(a[index2])=="date") ? a[index2] - b[index2] : a[index2].localeCompare(b[index2])
			}
			return ($.type(a[index1])=="number"||$.type(a[index1])=="date") ? a[index1] - b[index1] : a[index1].localeCompare(b[index1])
		} else {
			if(a[index1] == b[index1] && index2) {
				return ($.type(a[index2])=="number"||$.type(a[index2])=="date") ? b[index2] - a[index2] : b[index2].localeCompare(a[index2])
			}
			return ($.type(a[index1])=="number"||$.type(a[index1])=="date") ? b[index1] - a[index1] : b[index1].localeCompare(a[index1])
		}
	}
	return obj.sort(sortByIndex); //此处传入的参数是一个函数
}

function numToShort(num, flag) {
	//根据国际单位制词头缩写过长数字
	var negative = 0;
	if(num < 0) {
		negative = 1;
		num = Math.abs(num);
	}
	if ((num == 0) || (num == null)) {
		return "0";
	}
	var k = (flag===true)?1000:1024;
	if(num < k) {
		return "" + num.toFixed(0);
	}
	var size = ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'];
	var i = Math.floor(Math.log(num) / Math.log(k));
	return Math.pow(-1, negative) * (num / Math.pow(k, i)).toPrecision(3) + size[i];
}

// 对传入drawHighchart函数的data处理
function numChange(d){
	for(var x in d){
		var name = d[x].name;
		if(name.search('包数') == -1){
			for(var i in d[x].data){
				var ss = d[x].data[i];
				if(ss instanceof Array){
					var num = d[x].data[i][1];
					if(num < 0) {
						d[x].data[i] = [d[x].data[i][0], Math.abs(num)];
					}
					if ((num == 0) || (num == null)) {
						d[x].data[i] =  [d[x].data[i][0], 0];
					}
					var k = 1024;
					if(num < k) {
						d[x].data[i] = [d[x].data[i][0], parseInt(num.toFixed(0))];
					}
					else if(num>=k && num<Math.pow(k, 2)){
						d[x].data[i] = [d[x].data[i][0],num/1.024];
					}
					else if(num>=Math.pow(k, 2) && num<Math.pow(k, 3)){
						d[x].data[i] = [d[x].data[i][0],num/Math.pow(1.024, 2)];
					}
					else if(num>=Math.pow(k, 3) && num<Math.pow(k, 4)){
						d[x].data[i] = [d[x].data[i][0],num/Math.pow(1.024, 3)];
					}
					else if(num>=Math.pow(k, 4) && num<Math.pow(k, 5)){
						d[x].data[i] = [d[x].data[i][0],num/Math.pow(1.024, 4)];
					}
					else if(num>=Math.pow(k, 5) && num<Math.pow(k, 6)){
						d[x].data[i] = [d[x].data[i][0],num/Math.pow(1.024, 5)];
					}
					else{
						d[x].data[i] = [d[x].data[i][0],num];
					}
				}
				else if(ss instanceof Object){
					var num = d[x].data[i].y;
					if(num < 0) {
						d[x].data[i] = {'x':d[x].data[i].x, 'y': Math.abs(num)};
					}
					if ((num == 0) || (num == null)) {
						d[x].data[i] = {'x':d[x].data[i].x, 'y':0};
					}
					var k = 1024;
					if(num < k) {
						d[x].data[i] = {'x':d[x].data[i].x, 'y':parseInt(num.toFixed(0))};
					}
					else if(num>=k && num<Math.pow(k, 2)){
						d[x].data[i] = {'x':d[x].data[i].x, 'y':num/1.024}
					}
					else if(num>=Math.pow(k, 2) && num<Math.pow(k, 3)){
						d[x].data[i] = {'x':d[x].data[i].x, 'y':num/Math.pow(1.024, 2)};
					}
					else if(num>=Math.pow(k, 3) && num<Math.pow(k, 4)){
						d[x].data[i] = {'x':d[x].data[i].x, 'y':num/Math.pow(1.024, 3)};
					}
					else if(num>=Math.pow(k, 4) && num<Math.pow(k, 5)){
						d[x].data[i] = {'x':d[x].data[i].x, 'y':num/Math.pow(1.024, 4)}
					}
					else if(num>=Math.pow(k, 5) && num<Math.pow(k, 6)){
						d[x].data[i] = {'x':d[x].data[i].x, 'y':num/Math.pow(1.024, 5)}
					}
					else{
						d[x].data[i] = {'x':d[x].data[i].x, 'y':num};
					}
				}
			}
		}
	}
	return d;
}

function numToChart(data) {
	if(data instanceof Array){
		for(var i in data){
			var num = data[i]['bit_count'];
			if(num < 0) {
				 data[i]['bit_count'] = Math.abs(num);
			}
			if ((num == 0) || (num == null)) {
				 data[i]['bit_count'] =  0;
			}
			var k = 1024;
			if(num < k) {
				 data[i]['bit_count'] = num.toFixed(0);
			}
			else if(num>=k && num<Math.pow(k, 2)){
				 data[i]['bit_count'] = num/1.024
			}
			else if(num>=Math.pow(k, 2) && num<Math.pow(k, 3)){
				 data[i]['bit_count'] = num/Math.pow(1.024, 2)
			}
			else if(num>=Math.pow(k, 3) && num<Math.pow(k, 4)){
				 data[i]['bit_count'] = num/Math.pow(1.024, 3)
			}
			else if(num>=Math.pow(k, 4) && num<Math.pow(k, 5)){
				 data[i]['bit_count'] = num/Math.pow(1.024, 4)
			}
			else if(num>=Math.pow(k, 5) && num<Math.pow(k, 6)){
				 data[i]['bit_count'] = num/Math.pow(1.024, 5)
			}
			else{
				data[i]['bit_count'] = num;
			}
		}
	}
	else{
		for(var key in data){
			for(var i in data[key]){
				var num = data[key][i]['bit_count'];
				if(num < 0) {
					 data[key][i]['bit_count'] = Math.abs(num);
				}
				if ((num == 0) || (num == null)) {
					 data[key][i]['bit_count'] =  0;
				}
				var k = 1024;
				if(num < k) {
					data[key][i]['bit_count'] = num.toFixed(0);
				}
				else if(num>=k && num<Math.pow(k, 2)){
					data[key][i]['bit_count'] = num/1.024
				}
				else if(num>=Math.pow(k, 2) && num<Math.pow(k, 3)){
					data[key][i]['bit_count'] = num/Math.pow(1.024, 2)
				}
				else if(num>=Math.pow(k, 3) && num<Math.pow(k, 4)){
					data[key][i]['bit_count'] = num/Math.pow(1.024, 3)
				}
				else if(num>=Math.pow(k, 4) && num<Math.pow(k, 5)){
					data[key][i]['bit_count'] = num/Math.pow(1.024, 4)
				}
				else if(num>=Math.pow(k, 5) && num<Math.pow(k, 6)){
					data[key][i]['bit_count'] = num/Math.pow(1.024, 5)
				}
				else{
					data[key][i]['bit_count'] = num;
				}
			}
		}
	}
}

 //验证IP函数
function isValidIP(ip){
	var reg =  /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
	return reg.test(ip);
}

//验证ip掩码
function checkMask(mask){
  var reg=/^(254|252|248|240|224|192|128|0)\.0\.0\.0$|^(255\.(254|252|248|240|224|192|128|0)\.0\.0)$|^(255\.255\.(254|252|248|240|224|192|128|0)\.0)$|^(255\.255\.255\.(255|254|252|248|240|224|192|128|0))$/;
  return reg.test(mask)
}

//判断数组是否重复
function isRepeat(arr){
	var hash = {};
	for(var i in arr) {
		if(hash[arr[i]])
			return true;
		hash[arr[i]] = true;
	}
	return false;
}

//是否为正整数
function isPositiveInteger(s){
     var re = /^[0-9]+$/ ;
     return re.test(s)
}


//验证mac函数
function isValidMac(mac) {
    var reg = /[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}/;
    return reg.test(mac);
}

function pagePermission(permission_list){
	var data = [];
	$.each(permission_list, function(key, value){
		if(value==='switchManage'){
			data.push(['交换机管理', value]);
		}
		else if(value==='traffic'){
			data.push(['流量管理', value]);
		}
		else if(value==='tenantManage'){
			data.push(['租户管理', value]);
		}
		else if(value==='subAccountManage'){
			data.push(['子账号管理', value]);
		}
		else if(value==='loadBalance'){
			data.push(['负载均衡管理', value]);
		}
		else if(value==='tokenManage'){
			data.push(['token管理', value]);
		}
		else if(value==='defendIp'){
			data.push(['高防管理', value]);
		}
		else if(value==='multilineManage'){
			data.push(['多线管理', value]);
		}
		else if(value==='businessManage'){
			data.push(['业务管理', value]);
		}
		else if(value==='resourceManage'){
			data.push(['资源管理', value]);
		}
		else if(value==='idcUserPage'){
			data.push(['用户页面管理', value]);
		}
	});
	return data.reverse();
}

function ts_to_str(st){
	var date = new Date(st*1000);
	var Y = date.getFullYear() + '-';
	var M = (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1) + '-';
	var D = (date.getDate() < 10 ? '0'+date.getDate() : date.getDate()) + ' ';
	var h = (date.getHours() < 10 ? '0'+date.getHours() : date.getHours()) + ':';
	var m = (date.getMinutes() < 10 ? '0'+date.getMinutes() : date.getMinutes()) + ':';
	var s = (date.getSeconds() < 10 ? '0'+date.getSeconds() : date.getSeconds());
	return (Y+M+D+h+m+s);
}



















