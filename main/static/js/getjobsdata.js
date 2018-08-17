/**
 * Created by samsung1 on 2018/5/8.
 */
var comTable =  $('#dataTable').DataTable({
        ajax: '/getjobsdata_run_hisdata',
        columns: [
            { title: "序号" },
            { title: "数据源网站" },
            { title: "数据条件" },
            { title: "时间间隔" },
            { title: "启动时间" },
            { title: "操作人员" },
            { title: "运行状态" },
            { title: "停止时间" },
            { title: "操作",
              render:function (data, type, full, meta) {
                    return "<button id='stop' type='submit' class='btn btn-success' value="+full[0]+">stop</button>  "
                }
            }
        ],
        responsive: true,
        deferRender: true
    });

$('#dataTable tbody').on( 'click', '#stop', function () {
    var id =$(this).attr('value');
    data = JSON.stringify({'id':id});
    console.log(data);
    $.ajax({
        "type":'POST',
        "url": '/change_hisjobstatus',
        "data": data,
        success:function (data_r) {
            data_res = jQuery.parseJSON(data_r);
            if (data_res['code'] == 500) {
                alert(data_res['message'])
            } else {
               location.href = "/getjobsdata_run_his";
            }
        }
    })
});

$('#run_script').click(function () {
    var web_data = $('#web_data').val();
    var data_filter = $('#data_filter').val();
    var every_time = $('#everytime').val();
    console.log(web_data);
    console.log(data_filter);
    console.log(every_time);
    data_in = JSON.stringify({'web_data':web_data,'data_filter':data_filter,'every_time':every_time});
    $.post("/insert_rundata",data_in,function(data) {
        data = jQuery.parseJSON(data);
        if (data['code']==500){
            alert(data['message']);
        }else{
            alert("脚本已运行！");
            document.location.href='/getjobsdata_run_his';
        }
    })
});

$('#add_getdata').click(function (){
    $("#infoModal").modal();
});