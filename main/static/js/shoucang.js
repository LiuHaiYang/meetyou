/**
 * Created by samsung1 on 2018/5/24.
 */
var comTable =  $('#dataTable').DataTable({
        ajax: '/home/shoucang_list_data',
       columns: [
            { title: "职位名称" },
            { title: "公司名称" },
            { title: "公司类型" },
            { title: "学历" },
            { title: "薪资" },
            { title: "工作经验" },
            { title: "公司地址"},
            { title: "发布平台" },
            { title: "发布时间" },
            { title: "操作",
              render:function (data, type, full, meta) {
                    return   "<button id='delete' type='submit' class='btn btn-primary' value="+full[9]+">删除</button>"
                }
            }
        ],
        responsive: true,
        deferRender: true
    });

$('#dataTable tbody').on( 'click', '#delete', function () {
    var id =$(this).attr('value');
    var platform =$(this).parent().parent().find('td').eq(7).text();
    data = JSON.stringify({'id':id,'platform':platform});
    console.log(data);
    $.ajax({
        "type":'POST',
        "url": '/home/changejobinfo_status',
        "data": data,
        success:function (data_r) {
            data_res = jQuery.parseJSON(data_r);
            console.log(data_res)
            if (data_res['code'] == 500) {
                alert(data_res['message'])
            } else {
                alert('成功删除！')
               window.location.href = '/home/shoucang_list'
            }
        }
    })
    $("#infoModal").modal();
});