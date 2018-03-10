/*左侧菜单点击*/

/*获取宽度*/
function tabWidth(tabarr) {
    var allwidth = 0;
    $(tabarr).each(function() {
        allwidth += $(this).outerWidth(true)
    });
    return allwidth;
}

/*头部下拉框移入移出*/
$(document).on("mouseenter",".header-bar-nav",function(){
    $(this).addClass("open");
});
$(document).on("mouseleave",".header-bar-nav",function(){
    $(this).removeClass("open");
});

/*左侧菜单展开和关闭按钮事件*/
$(document).on("click",".layout-side-arrow",function(){
    if($(".layout-side").hasClass("close")){
        $(".layout-side").removeClass("close");
        $(".layout-main").removeClass("full-page");
        $(".layout-footer").removeClass("full-page");
    }else{
        $(".layout-side").addClass("close");
        $(".layout-main").addClass("full-page");
        $(".layout-footer").addClass("full-page");
    }
});

/*头部菜单按钮点击事件*/
$(".header-menu-btn").click(function(){
    $(".layout-side").removeClass("close");
    $(".layout-main").removeClass("full-page");
    $(".layout-footer").removeClass("full-page");
    $(".layout-side").slideToggle();
});

/*左侧菜单响应式*/
$(window).resize(function() {
    var width = $(this).width();
    if(width >= 750){
        $(".layout-side").show();
    }else{
        $(".layout-side").hide();
    }
});

/*获取cookie中的皮肤*/
function getSkinByCookie(){
    var v = getCookie("scclui-skin");
    var hrefStr=$("#layout-skin").attr("href");
    if(v == null || v == ""){
        v="qingxin";
    }
    if(hrefStr != undefined){
        var hrefRes=hrefStr.substring(0,hrefStr.lastIndexOf('skin/'))+'skin/'+v+'/skin.css';
        $("#skin").attr("href",hrefRes);
    }
}

$("#idc_ul").on("click","li",function(event){
    var name=$(event.currentTarget).find("a").attr("id");
    $.ajax({
        url:'/user/select_idc',
        type:'post',
        data:{idc:name},
        success:function(result){
            if(result.success==1){
                window.location.reload();
            }
            else{
                alert(result.err_msg);
            }
        },
        error:function(){
            $("#err_message").empty().text("对不起，读取数据错误").slideDown("500");
            setTimeout(function(){
                $("#err_message").slideUp('600');
            },2000)
        }
    })
})


function handle_idc_href(name, url){
    $.ajax({
        url:'/user/select_idc',
        type:'post',
        data:{idc:name},
        success:function(result){
            if(result.success==1){
                window.location.reload();
                location.href = url;
            }
            else{
                alert(result.err_msg);
            }
        }
    });
}