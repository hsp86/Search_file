$(function(){
    // 将网页中指定元素中的指定字符串标添加span来显示指定class的颜色
    function set_color($obj,str)
    {
        obj_str = $obj.text();
        $obj.html(obj_str.replace(new RegExp(str,'g'),'<span class="set_color">' + str + '</span>'));

    }
    // 搜索结果点击事件，每次加载后需要重新绑定
    function re_bind()
    {
        $('.result_item').bind('click',function(event) {
            open_file($(this).children('.item_fname').text());
        });
    }
    // 将网页中选中checkbox内容转化为ajax格式字符串返回
    function get_search_dir(class_text)
    {
        var re_var = "";
        $('.' + class_text).each(function(index, el) {
            if(this.checked)
            {
                re_var = re_var + "&dir=" + this.value;
            }
        });
        return re_var;
    }
    // 搜索内容，通过ajax发送搜索文本和目录
    function search(search_text)
    {
        var method = "get";
        var action = '/search';
        var search_data = "search_text=" + search_text + get_search_dir('check_dir');
        $('.search_result').html("正在搜索...");
        // alert(search_data);
        $.ajax({
            url: action,
            type: method,
            data: search_data,
            success: function(msg){
                $('.search_result').html(msg);
                re_bind();
                set_color($('.item_fcontent'),search_text);
            }
        });
    }
    // 打开文件，通过ajax发送文件名获取文件内容
    function open_file(file)
    {
        var method = "get";
        var action = '/open_file';
        var file_name = "file_name=" + file;
        $.ajax({
            url: action,
            type: method,
            data: file_name,
            success: function(text){
                $('.file_name').text(file);
                $('.file_content').html(text);
                $('.showfile').css({display: 'block'});
                set_color($('.file_content'),search_text);
            }
        });
    }
    // 搜索按钮点击事件
    search_text = ""
    $('#search_button').bind('click', function(event) {
        search_text = $('#search_text').val();
        search(search_text);
    });
    // 显示文件内容中关闭按钮点击事件
    $('.close').bind('click',function(event) {
        $('.showfile').css({display: 'none'});
    });
})
