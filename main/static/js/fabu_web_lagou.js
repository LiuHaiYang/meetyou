/**
 * Created by samsung1 on 2018/5/7.
 */
var comTable =  $('#dataTable').DataTable({
        ajax: '/companys/lagouweb_datas',
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
                    return "<button id='info' type='submit' class='btn btn-success' value="+full[9]+">详情</button>  "
                }
            }
        ],
        responsive: true,
        deferRender: true
    });

$('#dataTable tbody').on( 'click', '#info', function () {
    var id =$(this).attr('value');
    var platform =$(this).parent().parent().find('td').eq(7).text();
    data = JSON.stringify({'id':id,'platform':platform});
    console.log(data);
    $.ajax({
        "type":'POST',
        "url": '/getjobinfo',
        "data": data,
        success:function (data_r) {
            data_res = jQuery.parseJSON(data_r);
            console.log(data_res)
            if (data_res['code'] == 500) {
                alert(data_res['message'])
            } else {
                var data_re = data_res['data'][0]
                $('#zhaopinid').val(data_re[0]);
                $('#zhaopinzhiwei').val(data_re[5]);
                $('#companyname').val(data_re[2]);
                $('#rongzi').val(data_re[4]);
                $('#fabutime').val(data_re[6]);
                $('#jobyouhuo').val(data_re[11]);
                $('#xueli').val(data_re[12]);
                $('#money').val(data_re[13]);
                $('#worktime').val(data_re[14]);
                $('#companyaddress').val(data_re[8]);
                $('#jobyaoqiu').val(data_re[9]);
                $('#workzhize').val(data_re[10]);
                $('#jobdesc').val(data_re[15]);
                $('#companyjianjie').val(data_re[16]);
            }
        }
    })
    $("#infoModal").modal();
});

$('#addlove').click(function () {
    var ids = $('#zhaopinid').val();
    var id = '拉勾-'+ids
    data = JSON.stringify({'id':id});
     $.ajax({
        "type":'POST',
        "url": '/addlove_list',
        "data": data,
        success:function (data_r) {
            data_res = jQuery.parseJSON(data_r);
            if (data_res['code'] == 500) {
                alert(data_res['message'])
            } else {
                alert('已加入收藏！')
                // window.location.href = '/companys/lagouweb'
            }
        }
    })
});