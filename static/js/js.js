$(function(){
    // 将网页中指定元素中的指定字符串标添加span来显示指定class的颜色
    function set_color($obj,str)
    {
        $obj.each(function(index, el) {
            // 虽然在python中转换过，但是这里又重新重html中获取text又变会正常字符了，所以再次转换
            // 这个转换主要针对function search(search_text)中调用（function open_file(file)中不这样转换也正常）
            // 而在function search(search_text)中不这样转换则出错，因为这里面用的.html插入会将如&lt;转换为正常字符如<，
            // 这里再用.text获取的字符就为正常字符如<(而open_file中用.text插入则仍为如&lt;),
            // 这里再以.html方式插入就转换为html代码了，所以要再次转换
            obj_str =$(this).text().replace(new RegExp('<','g'),'&lt;').replace(new RegExp('>','g'),'&gt;');
            $(this).html(obj_str.replace(new RegExp(str,'g'),'<span class="set_color">' + str + '</span>'));
        });

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
        $('.svg').css({display: 'block'}); // 加载前显示等待动画
        // alert(search_data);
        $.ajax({
            url: action,
            type: method,
            data: search_data,
            success: function(msg){
                $('.svg').css({display: 'none'}); // 加载完隐藏等待动画
                $('.search_result').html(msg);
                re_bind();
                set_color($('.item_fcontent'),search_text);
                set_color($('.item_fname'),search_text);// 同时也要标亮文件名中搜索的字符串
            }
        });
    }
    // 打开文件，通过ajax发送文件名获取文件内容
    function open_file(file)
    {
        var method = "get";
        var action = '/open_file';
        var file_name = "file_name=" + file;
        $('.svg').css({display: 'block'}); // 加载前显示等待动画
        $.ajax({
            url: action,
            type: method,
            data: file_name,
            success: function(text){
                $('.svg').css({display: 'none'}); // 加载完隐藏等待动画
                $('.file_name').text(file);
                $file_cont_pre = $('.file_content pre');
                $file_cont_pre.text(text);
                $('.showfile').css({display: 'block'});
                set_color($file_cont_pre,search_text);
                set_color($(".file_name"),search_text);// 同时也要标亮文件名中搜索的字符串
            }
        });
    }
    // 搜索按钮点击事件
    search_text = ""
    $('#search_button').bind('click', function(event) {
        search_text = $('#search_text').val();
        search(search_text);
    });
    $('#search_text').bind('keydown',function(event) {
        if(event.keyCode == 13)
        {
            $('#search_button').click();
        }
    });
    // 显示文件内容中关闭按钮点击事件
    $('.close').bind('click',function(event) {
        $('.showfile').css({display: 'none'});
    });
    // 加载前都显示svg动画，加载完就结束svg动画
    $('.svg').css({display: 'none'}); // 加载完隐藏等待动画
})
