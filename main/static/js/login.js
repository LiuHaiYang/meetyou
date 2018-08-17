/**
 * Created by sa on 18-05-05.
 */
define(function (require,exports,module) {
    require("bootstrap");
    var ajax = require("js/ajax");
    var Vue = require("lib/vue.min");
    var app = new Vue({
        el:"#login",
        delimiters:['<%=','%>'],
        data:{
            data:{
                email:"",
                password:""
            }
        },
        methods:{
            getCaptcha:function () {
                var _this = this;
                ajax("get","/publisher/captcha",null,function (res) {
                    var data = JSON.parse(res);
                    if(data.status==200){
                        var data = JSON.parse(res);
                        data.data.captcha.captcha_image = "data:image/png;base64,"+ data.data.captcha.captcha_image;
                        _this.data.captcha = data.data.captcha
                    }else{

                    }
                });
            },
            onSubmit:function () {
                if(this.data.email==""){
                    $("#content_modal").html("Please input email");
                    $('.modal').modal("toggle");
                    return;
                }
                if(this.data.password==""){
                    $("#content_modal").html("Please input password");
                    $('.modal').modal("toggle");
                    return;
                }
                var _this = this;
                ajax("post","/api/v1/loginAPI",JSON.stringify(this.data),function (res) {
                    var data = JSON.parse(res);
                    if(data.code==200){
                        location.href = "/home";
                    }else {
                        $("#content_modal").html(data.message);
                        $('.modal').modal("toggle");
                    }
                })
            }
        }
    });
});