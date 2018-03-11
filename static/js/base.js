$(function(){

    //前端页面展示权限
    var permission_obj = ['topo','blogManage','userManage','commitManage','bulletinManage'];
    for (var i in permission_obj) {
        if (permission_obj[i] === 'topo') {
            $("#topo").removeClass('hidden');
        }
        if (permission_obj[i] === 'blogManage') {
            $("#blog-manage").removeClass('hidden');
        }
        if (permission_obj[i] === 'userManage') {
            $("#user-manage").removeClass('hidden');
        }
        if (permission_obj[i] === 'commitManage') {
            $("#commit-manage").removeClass('hidden');
        }
        if (permission_obj[i] === 'bulletinManage') {
            $("#bulletin-manage").removeClass('hidden');
        }
    }

});

/*随机颜色*/
function getMathColor(){
    var arr = new Array();
    arr[0] = "#ffac13";
    arr[1] = "#83c44e";
    arr[2] = "#2196f3";
    arr[3] = "#e53935";
    arr[4] = "#00c0a5";
    arr[5] = "#16A085";
    arr[6] = "#ee3768";

    var le = $(".menu-item > a").length;
    for(var i=0;i<le;i++){
        var num = Math.round(Math.random()*5+1);
        var color = arr[num-1];
        $(".menu-item > a").eq(i).find("i:first").css("color",color);
    }
}

