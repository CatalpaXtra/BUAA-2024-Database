$(function () {
    function loginBtnClick() {
        $("#login").click(function (event) {
            event.preventDefault();
            let email = $("input[name='email']").val();
            if (!email) {
                alert("请先输入邮箱！");
                return;
            }
            let password = $("input[name='password']").val();
            if (!password) {
                alert("请先输入密码！");
                return;
            }
            let remember = $("input[name='remember']").is(':checked') ? 1 : 0;

            $.ajax('/user/login/check/' + email + '/' + password + '/' + remember, {
                method: 'GET',
                success: function(result){
                    if(result['code'] == 200){
                        window.location.href = '/';
                    }else{
                        alert(result['message']);
                    }
                },
                error: function (error){
                    console.log(error);
                    alert('请求失败，请稍后再试！');
                }
            })
        });
    }

    loginBtnClick();
});
