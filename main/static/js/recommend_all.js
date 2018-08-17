/**
 * Created by samsung1 on 2018/5/26.
 */
var comTable =  $('#dataTable').DataTable({
        ajax: '/recommend_all_data',
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