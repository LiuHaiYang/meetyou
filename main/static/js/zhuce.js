/**
 * Created by samsung1 on 2018/5/6.
 */
$("#zhuce_user").click(function () {
    var email = $("#email").val();
    var pwd = $("#pwd").val();
    var pwd_t = $("#pwd_t").val();
    var number = $("#number").val();
    var jiaose = $("#zhuce_player").val();
    var yanzheng = $("#yanzheng").val();
    // console.log(email);

    if (number == "" || pwd == "" || email == "") {
        alert("注册信息不能为空!")
    } else {
           if (jiaose == '1' ) {
                if (yanzheng !='9999'){
                    alert("注册管理员，请输入正确的验证码！!")
                    return false;
                }

            }else{
                if (yanzheng ){
                    alert("注册普通用户，无需验证码！!")
                    return false;
                }

            }
            if (pwd != pwd_t) {
                alert("密码不一致！!")
                return false;
            }
        var p_data = {"email":email,"pwd":pwd,"number":number,"jiaose":jiaose}
        $.ajax({
            async: true,
            url: "/zhuceinfo",
            type: "POST",
            data: JSON.stringify(p_data),
            dataType: "json",
            success: function (results) {
                if (results['code'] == 500) {
                    alert(results['message'])
                } else {
                    alert("注册成功，请登录!");
                    window.location.href = '/login';
                }
            }
        })
    }
});