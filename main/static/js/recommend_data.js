/**
 * Created by samsung1 on 2018/5/15.
 */
$('#xietong_recommend').click(function () {
    document.location.href='/recommend_xietongdata';
})
var comTable =  $('#dataTable').DataTable({
        ajax: '/recommend_query_all',
        columns:[
            { title: "职位序号" },
            { title: "推荐用户ID" },
            { title: "平台" },
            { title: "职位名称" },
            { title: "公司名称" },
            { title: "薪资" },
            { title: "工作经验" },
            { title: "城市" },
            { title: "职位诱惑" }
        ],
        responsive: true,
        deferRender: true
    });