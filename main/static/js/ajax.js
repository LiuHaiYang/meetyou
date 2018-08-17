/**
 * Created by sa on 16-12-6.
 */
define(function (require,exports,module) {
    var $ = require("jquery");
    var ajax = function (method,url,data,cb) {
        $.ajax({
            url:url,
            method:method,
            beforeSend:function () {
                $(".mask").show();
            },
            data:data,
            success:function (data) {
                $(".mask").hide();
                cb&&cb(data);
            },
            error:function () {
                $(".mask").hide();
            }
        })
    }
    module.exports = ajax;
});