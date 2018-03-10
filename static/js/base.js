$(document).ready(function(){

    get_apply_permission();

    //前端页面展示权限
    function display_page_nav() {
        var permission_obj = eval($('#personal_permission').val());

        for (var i in permission_obj) {
            if (permission_obj[i] === 'traffic') {
                $('#topo').removeClass('hidden');
                $('#iplist').removeClass('hidden');
                $('#tenantlist').removeClass('hidden');
            }
            else if (permission_obj[i] === 'tenantManage') {
                $('#tenant-manage').removeClass('hidden');
            }
            else if (permission_obj[i] === 'loadBalance') {
                $('#load_balance').removeClass('hidden');
            }
            else if (permission_obj[i] === 'tokenManage') {
                $('#token_manage').removeClass('hidden');
            }
            else if (permission_obj[i] === 'defendIp') {
                $('#defend_ip_page').removeClass('hidden');
            }
            else if (permission_obj[i] === 'multilineManage') {
                $('#multiline_manage').removeClass('hidden');
            }
            else if (permission_obj[i] === 'switchManage') {
                $('#switch-manage').removeClass('hidden');
                $('#drop-switch-content').removeClass('hidden');
            }
            else if (permission_obj[i] === 'businessManage') {
                $('#business-manage').removeClass('hidden');
                $('#drop-business-content').removeClass('hidden');
            }
            else if (permission_obj[i] === 'resourceManage') {
                $('#resource-manage').removeClass('hidden');
                $('#drop-resource-content').removeClass('hidden');
            }
            else if (permission_obj[i] === 'idcUserPage') {
                $('#idc-system').removeClass('hidden');
            }
        }
        //版本都可见
        $('#version').removeClass('hidden');

        //业务管理
        $('#business-manage').click(function () {
            $(".menu-item").removeClass("active");
            $("#business-manage").addClass("active");
            $('#drop-resource-content').slideUp();
            $('#drop-switch-content').slideUp();
            $('#drop-workorder-content').slideUp();
            $('#drop-business-content').slideDown();

        });

        //工单管理
        $('#workorder-manage').click(function () {
            $(".menu-item").removeClass("active");
            $("#workorder-manage").addClass("active");
            $('#drop-resource-content').slideUp();
            $('#drop-switch-content').slideUp();
            $('#drop-business-content').slideUp();
            $('#drop-workorder-content').slideDown();

        });

        //资源管理
        $('#resource-manage').click(function () {
            $(".menu-item").removeClass("active");
            $("#resource-manage").addClass("active");
            $('#drop-business-content').slideUp();
            $('#drop-switch-content').slideUp();
            $('#drop-workorder-content').slideUp();
            $('#drop-resource-content').slideDown();
        });

        //交换机管理
        $('#switch-manage').click(function () {
            $(".menu-item").removeClass("active");
            $("#switch-manage").addClass("active");
            $('#drop-business-content').slideUp();
            $('#drop-resource-content').slideUp();
            $('#drop-workorder-content').slideUp();
            $('#drop-switch-content').slideDown();
        });
    }
    function get_apply_permission(){
        $.ajax({
            url: '/business_manage/apply_permission',
            success:function(res){
                if(res.success===1){
                    var data = res.data;
                    if(data['all_power']===true){
                        $('#workorder-manage').removeClass('hidden');
                        $('#drop-workorder-content').removeClass('hidden');
                    }
                    else{
                        $('#workorder-manage, #drop-workorder-content').remove();
                        var insert_html = '',
                            exist_html = '<li class="menu-item" id="to_do_workorder"><a href="/business_manage/my_order"><i class="icon-font">&#xe74b;</i><span>待办工单事项</span></a></li>';
                        if(data['work_orders'].length>0){
                            insert_html += '<li class="menu-item" id="create_workorder"><a href="/business_manage/apply"><i class="icon-font">&#xe64f;</i><span>创建工单</span></a></li>' + exist_html +
                                '<li class="menu-item" id="expire_workorder"><a href="/business_manage/expire_info"><i class="icon-font">&#xe6a8;</i><span>到期工单</span></a></li>';
                        }
                        else{
                            insert_html += exist_html;
                        }
                        if(data['rank']===10){
                            insert_html += '<li class="menu-item" id="all_department_workorder"><a href="/business_manage/order_index"><i class="icon-font">&#xe64b;</i><span>部门所有工单</span></a></li>';
                        }
                        $('ul.side-menu').prepend(insert_html);
                    }
                    display_page_nav();
                    getMathColor();
                    //渲染新建工单页面
                    if($('#form_content').length>0){
                        var get_data = data['work_orders'];
                        for(var i in get_data){
                            var insert_nav = '<li data-name="'+get_data[i]['name']+'"><span class="icon-font">&#xe64f;</span> <span class="current_text">'+ get_data[i]['name'] +'</span> <button class="btn btn-xs btn-primary pull-right">快速新建</button></li>';
                            $('#my_nav').append(insert_nav);
                            var keys = get_data[i]['keys'];
                            if(!$.isEmptyObject(keys)){
                                $('#my_nav li[data-name="'+get_data[i]['name']+'"]').data('value', keys);
                            }
                        }
                    }
                }
                else{
                    new GHAlert({
                        content: '对不起，系统异常',
                        type: 'fail',
                        time: 2000
                    }).show();
                }
            }
        })
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

