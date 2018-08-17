/**
 * Created by samsung1 on 2018/5/7.
 */
var comTable =  $('#dataTable').DataTable({
        ajax: '/recommend_perinfo_all_p',
        columns:[
        // [i.id,i.username,i.sex,i.intersert_hangye,i.hope_money,i.hope_city,i.worktime,i.live_city,i.per_do,i.job_key,
        //  i.hpone_number,i.email,i.user_level,i.user_type,i.user_status]
            { title: "推荐ID" },
            { title: "用户名" },
            { title: "性别" },
            { title: "兴趣行业" },
            { title: "期望薪资" },
            { title: "工作经验" },
            { title: "居住城市" },
            { title: "期望城市" },
            { title: "职位关键词" },
            { title: "联系方式" },
            { title: "邮箱地址" },
            { title: "停止时间" },
            { title: "操作",
              render:function (data, type, full, meta) {
                    return "<button id='start' type='submit' class='btn btn-success' value="+full[0]+">启动</button>" +
                        "<button id='stop' type='submit' class='btn btn-success' value="+full[0]+">停止</button> "+
                  "<button id='delete' type='submit' class='btn btn-primary' value="+full[0]+">删除</button>"
                }
            }
        ],
        responsive: true,
        deferRender: true
    });
$('#add_info').click(function (){
    $("#infoModal").modal();
});

$('#add_userinfo').click(function (){
     data = JSON.stringify({
    'name':$('#name').val(),
    'sex':$('#sex').val(),
    'hangyexingqu':$('#hangyexingqu').val(),
    'hopemoney' :$('#hopemoney').val(),
    'phone' :$('#phone').val(),
    'live_city':$('#live_city').val(),
    'hope_city' :$('#hope_city').val(),
    'worktime':$('#worktime').val(),
    'per_do' :$('#per_do').val(),
    'email' :$('#email').val(),
    'job_key' :$('#job_key').val(),

     })
    console.log(data);
    $.ajax({
        "type":'POST',
        "url": '/recommend_perinfo_addinfo',
        "data": data,
        success:function (data_r) {
            data_res = jQuery.parseJSON(data_r);
            console.log(data_res)
            if (data_res['code'] == 500) {
                alert(data_res['data'])
            } else {
                document.location.href='/recommend_perinfo';
            }
        }
    })
});

$('#dataTable tbody').on( 'click', '#start', function () {
    data = JSON.stringify({
    'id': $(this).attr('value'),
     })
    console.log(data);
    $.ajax({
        "type":'POST',
        "url": '/recommend_perinfo_start',
        "data": data,
        success:function (data_r) {
            data_res = jQuery.parseJSON(data_r);
            console.log(data_res)
            if (data_res['code'] == 500) {
                alert(data_res['data'])
            } else {
                alert(data_res['data'])
                document.location.href='/recommend_perinfo';
            }
        }
    })
})
$('#dataTable tbody').on( 'click', '#stop', function () {
        data = JSON.stringify({
    'id': $(this).attr('value'),
     })
    console.log(data);
    $.ajax({
        "type":'POST',
        "url": '/recommend_perinfo_stop',
        "data": data,
        success:function (data_r) {
            data_res = jQuery.parseJSON(data_r);
            console.log(data_res)
            if (data_res['code'] == 500) {
                alert(data_res['data'])
            } else {
                alert(data_res['data'])
                document.location.href='/recommend_perinfo';
            }
        }
    })
})
$('#dataTable tbody').on( 'click', '#delete', function () {
    data = JSON.stringify({
    'id': $(this).attr('value'),
     })
    console.log(data);
    $.ajax({
        "type":'POST',
        "url": '/recommend_perinfo_changestatus',
        "data": data,
        success:function (data_r) {
            data_res = jQuery.parseJSON(data_r);
            console.log(data_res)
            if (data_res['code'] == 500) {
                alert(data_res['data'])
            } else {
                alert(data_res['data'])
                document.location.href='/recommend_perinfo';
            }
        }
    })
})