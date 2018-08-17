var comTable =  $('#dataTable').DataTable({
        ajax: '/api/v1/orgnizationdata',
        columns: [
            { title: "姓名" },
            { title: "花名" },
            { title: "部门" },
            { title: "职位" },
            { title: "电话" },
            { title: "邮箱" },
            { title: "操作",
              render:function (data, type, full, meta) {
                    return "<button id='edit' type='submit' class='btn btn-success' value="+full[6]+">Edit</button>  "+"<button id='delete' class='btn btn-primary' value="+full[6]+">Delete</button>"
                }
            },
            { title: "最近操作时间" },
            { title: "所属部门" }
        ],
        "columnDefs": [
            {
                "targets": [ 8 ],
                "bFilter": true,
                "visible": false
            },
            {
                "targets": [4,5,7],
                "searchable": false
            }
        ],
        responsive: true,
        deferRender: true
    });

$('#dataTable tbody').on( 'click', '#edit', function () {
    var id = $(this).val();
    $('#empolyeeId').val(id);
    $('#name').val($(this).parent().parent().find('td').eq(0).text());
    $('#alisa').val($(this).parent().parent().find('td').eq(1).text());
    $('#department').val($(this).parent().parent().find('td').eq(2).text());
    $('#position').val($(this).parent().parent().find('td').eq(3).text());
    $('#phone').val($(this).parent().parent().find('td').eq(4).text());
    $('#email').val($(this).parent().parent().find('td').eq(5).text());
    $("#editModal").modal();
});

$('#department').keyup(function(){
    var depart = $("#department");
    var target = depart.siblings(".dropdown").find(".dropdown-menu");
    $.ajax({
            "type": "POST",
            "url": "/api/v1/allDepart",
            "data": {"department": depart.val()},
            "success": function(data){
                data = JSON.parse(data);
                if (!data) return;
                target.html("");
                for (var i in data){
                    !(function(i) {
                        target.append($("<li><a href='#'>" + i + "</a></li>").click(function () {
                            depart.val(data[i]);
                            target.hide();
                            return false;
                        }));
                    })(i)
                }
                target.show()
            }
        })
});

$('#position').keyup(function(){
    var position = $("#position");
    var target = position.siblings(".dropdownPO").find(".dropdown-menu");
    $.ajax({
            "type": "POST",
            "url": "/api/v1/allPosition",
            "data": {"position": position.val()},
            "success": function(data){
                data = JSON.parse(data);
                if (!data) return;
                target.html("");
                for (var i in data){
                    !(function(i) {
                        target.append($("<li><a href='#'>" + i + "</a></li>").click(function () {
                            position.val(data[i]);
                            target.hide();
                            return false;
                        }));
                    })(i)
                }
                target.show()
            }
        })
});

$('#dataTable tbody').on('click','#delete',function () {
    var id = $(this).val();
    alert('确定要删除该同学吗?');
    data = JSON.stringify({'id':id});
    $.post("/api/v1/deleteEmployee",data,function (data) {
        data = jQuery.parseJSON(data);
        if (data['code']==500){
            alert("删除失败!")
        }else{
            alert("删除成功!");
            comTable.ajax.url('/api/v1/orgnizationdata').load()
        }
    })
});

$('#editEmpolyee').click(function () {
    data = JSON.stringify({
        'name':$('#name').val(),
        'alias':$('#alisa').val(),
        'department': $('#department').val(),
        'position':$('#position').val(),
        'phone': $('#phone').val(),
        'email': $('#email').val(),
        'id': $('#empolyeeId').val()
    });
    $.post("/api/v1/updateEmployee",data,function(data) {
        data = jQuery.parseJSON(data);
        if (data['code']==500){
            alert(data['message']);
            comTable.ajax.url('/api/v1/orgnizationdata').load();
        }else{
            alert("修改成功！");
            $("#editModal").modal('hide');
            url = '/api/v1/orgnizationdata';
            comTable.ajax.url(url).load();
        }
    })
});

$('#addEmployee').click(function () {
    $("#editModal").modal();
    $('#name').val("");
    $('#alisa').val("");
    $('#department').val("");
    $('#position').val("");
    $('#phone').val("");
    $('#email').val("");
    $('#empolyeeId').val("")
});