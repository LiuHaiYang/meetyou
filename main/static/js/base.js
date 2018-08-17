define(function (require,exports,module) {
    var $ = require("jquery");
    var Vue = require("lib/vue.min");
    require("bootstrap");
    var header = new Vue({
        el:"#header",
        data:{
            isLogin:$(".isLogin").val()
        },
        delimiters:['<%=','%>']
    });
    $("#nav_nav").find("li").on("click",function () {
        $(this).addClass("active").siblings().removeClass("active");
    });

});