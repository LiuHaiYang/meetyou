/**
 * Created by samsung1 on 2018/5/23.
 */
var comTable =  $('#dataTable').DataTable({
        ajax: '/user_data_all',
        columns:[
            { title: "序号" },
            { title: "用户名" },
            { title: "用户级别" },
            { title: "联系电话" },
            { title: "创建时间" },
            { title: "最后登陆时间" },
            { title: "操作",
              render:function (data, type, full, meta) {
                    return "<button id='edit' type='submit' class='btn btn-success' value="+full[0]+">编辑</button>  " +
                        "<button id='delete' type='submit' class='btn btn-primary' value="+full[0]+">删除</button>"
                }
            }
        ],
        responsive: true,
        deferRender: true
    });

$('#dataTable tbody').on( 'click', '#delete', function () {
    var id =$(this).attr('value');
    data = JSON.stringify({'id':id});
    console.log(data);
    $.ajax({
        "type":'POST',
        "url": '/changeuserstatus',
        "data": data,
        success:function (data_r) {
            data_res = jQuery.parseJSON(data_r);
            console.log(data_res)
            if (data_res['code'] == 500) {
                alert(data_res['message'])
            } else {
                window.location='/userdata'
            }
        }
    })
});

$('#dataTable tbody').on( 'click', '#edit', function () {

     $('#user_id').val($(this).parent().parent().find('td').eq(0).text());
     $('#username').val($(this).parent().parent().find('td').eq(1).text());
     $('#user_phone').val($(this).parent().parent().find('td').eq(3).text());

     var p = $(this).parent().parent().find('td').eq(2).text();
        if(p=='管理员'){
            $("#zhuce_player").find("option:selected").text('管理员');
        }else{
            $("#zhuce_player").find("option:selected").text('普通用户');
        }
        $("#infoModal").modal();
});

$('#edit_userinfo').click(function () {
    data = JSON.stringify({
        'id':$('#user_id').val(),
        'user_name':$('#username').val(),
        'user_number':$('#user_phone').val(),
        'user_level':$('#zhuce_player').val()}
    );
    $.ajax({
        "type":'POST',
        "url": '/edituserinfo',
        "data": data,
        success:function (data_r) {
            data_res = jQuery.parseJSON(data_r);
            if (data_res['code'] == 500) {
                alert(data_res['message'])
            } else {
                window.location = '/userdata'
            }
        }
    })
    $("#infoModal").modal();
});
