/**
 * Created by sa on 18/04/17.
 */
define(function (require,exports,module) {
    /*
     获取 url 中的参数
     1. 指定参数名称，返回该参数的值 或者 空字符串
     2. 不指定参数名称，返回全部的参数对象 或者 {}
     3. 如果存在多个同名参数，则返回数组
    */
    var getUrlParam = function(sUrl, sKey) {
        var queryStr = sUrl.split("#")[0].split("?")[1];
        if(sKey&&queryStr){
            var arr =[];
            var queryStrSplit = queryStr.split("&");
            for(var i=0,len=queryStrSplit.length;i<len;i++){
                var newArr = queryStrSplit[i].split("=");
                if(newArr[0]==sKey){
                    arr.push(newArr[1]);
                }
            }
            if(arr.length==1){
                return arr[0]
            }else if(arr.length==0){
                return "";
            }
            return arr;
        }else{
            if(!queryStr){
                return Boolean(false);
            }else{
                var obj ={};
                var queryStrSplit = queryStr.split("&");
                for(var i=0,len=queryStrSplit.length;i<len;i++){
                    var newArr = queryStrSplit[i].split("=");
                    if(!obj.hasOwnProperty(newArr[0])){
                        obj[newArr[0]] =[];
                    }
                    obj[newArr[0]].push(newArr[1]);
                }
                return obj;
            }
        }
    }

    module.exports = {
        getUrlParam:getUrlParam
    }

})