      var flag = new Array(4);
      //ready函数
      $(function() {
        //开启新界面，判断是否已经登录。即判断loginStatus
        if($.cookie('loginStatus')=='1')
        {
          afterLogin();
        }
        else{
          $.cookie('loginStatus','0',{expires:1,path:'/'});
        }

        //点击退出登录按钮
        $("#unlogin").click(function () {

            afterUnlogin();
            warning('用户：'+$.cookie('nickName')+"已退出登录！");
            cookieClear();
        });
		
		$("#loginForm").children().bind('keydown',function () {
          	if(event.keyCode == "13")
            {
                login();
            }
        })

        //点击弹出登录框按钮
        $('#loginModalButton').click(function() {
          $('#loginModal').modal('show');
        });

        $('#loginButton').click(function(){
			login();
        });




        var errMsg;


        $.each($("#registerForm input"), function (i, val) {
           $(val).blur(function () {
             if ($(val).attr("name") == "nickName") {
               $(".nickMsg").remove();
               var nickName = val.value;
               var regName = /[\u4e00-\u9fa5]{2,6}/
               if (nickName == "" || nickName.trim() == "") {
                 errMsg = "<span class='nickMsg' style='color:red;'>昵称不能为空</span>";
                 flag[0]=0;
               }  else {
                 errMsg = "<span class='nickMsg' style='color:red;'>OK！</span>";
                 flag[0]=1;
               }
               $(this).parent().append(errMsg);
             } else if ($(val).attr("name") == "email") {
               $(".emailMsg").remove();
               var email = val.value;
               var regEmail = /^\w+@\w+((\.\w+)+)$/;
               if (email == "" || email.trim() == "") {
                 errMsg = "<span class='emailMsg' style='color:red;'>邮箱不能为空</span>";
                 flag[1]=0;
               } else if (!regEmail.test(email)) {
                 errMsg = "<span class='emailMsg' style='color:red;'>邮箱账号@域名。如good@tom.com、whj@sina.com.cn</span>";
                 flag[1]=0;
               } else {
                 errMsg = "<span class='emailMsg' style='color:red;'>OK！</span>";
                 flag[1]=1;
               }
               $(this).parent().append(errMsg);
             } else if ($(val).attr("name") == "pwd") {
               $(".pwdMsg").remove();
               var pwd = val.value;
               var regPwd = /^\w{4,10}$/;
               if (pwd == "" || pwd.trim() == "") {
                 errMsg = "<span class='pwdMsg' style='color:red;'>密码不能为空</span>";
                 flag[2]=0;
               } else if (!regPwd.test(pwd)) {
                 errMsg = "<span class='pwdMsg' style='color:red;'>格式错误</span>";
                 flag[2]=0;
               } else {
                 errMsg = "<span class='pwdMsg' style='color:red;'>OK！</span>";
               }
               $(this).parent().append(errMsg);
             } else if ($(val).attr("name") == "pwd2") {
               $(".pwd2Msg").remove();
               var pwd2 = $("#registerPwd2").val();
               var pwd = $("#registerPwd1").val();
               if (pwd2 == "" || pwd2.trim() == "" || pwd2 != pwd) {
                 errMsg = "<span class='pwd2Msg' style='color:red;'>两次输入密码不一致</span>";
                 flag[2]=0;
               } else {
                 errMsg = "<span class='pwd2Msg' style='color:red;'>OK！</span>";
                 flag[2]=1;
               }
               $(this).parent().append(errMsg);
             } else if ($(val).attr("name") == "phone") {
               $(".phoneMsg").remove();
               var phone = val.value;
               var regPhone = /[13,15,18]\d{9}/;
               if (phone == "" || phone.trim() == "") {
                 errMsg = "<span class = 'phoneMsg' style = 'color:red;' > 手机号不能为空 </span>";
                 flag[3]=0;
               } else if (!regPhone.test(phone)) {
                 errMsg = "<span class = 'phoneMsg' style = 'color:red;' > 格式错误 </span>";
                 flag[3]=0;
               } else {
                 errMsg = "<span class = 'phoneMsg' style = 'color:red;' > OK！ </span>";
                 flag[3]=1;
               }
               $(this).parent().append(errMsg);
             }
             if(flag[0]&&flag[1]&&flag[2]&&flag[3])
             {
               $('#registerSubmit').removeClass('btn-default');
               $('#registerSubmit').addClass('btn-primary');
               $('#registerSubmit').removeClass('disabled');
             }
             else
             {
               $('#registerSubmit').addClass('btn-default');
               $('#registerSubmit').removeClass('btn-primary');
               $('#registerSubmit').addClass('disabled');
             }
           });


     });

        $('#registerSubmit').click(function () {
          if($(this).hasClass('btn-default'))return;
          var registerData = {
            'nickName':$('#registerNickName').val(),
            'pwd':$('#registerPwd2').val(),
            'phone':$('#registerPhone').val(),
            'email':$('#registerEmail').val()
          };
          $.ajax({
            url: "{% url 'login:register' %}",
            //请求的url地址
            type:"post",
            //请求方式
            dataType: "json",
            //返回格式为json
            async: true,
            //请求是否异步，默认为异步，这也是ajax重要特性
            data: JSON.stringify(registerData),
            //参数值
            beforeSend: function() {
              //请求前的处理
            },
            success: function(data) {

              warning(data['content']);

            },
            complete: function() {
              //请求完成的处理
            },
            error: function() {
              //请求出错处理
              warning('请求出错');
            }
          })
        })


      });


      //其他函数
      function warning(content) {
        $('#warningContent').html('<h1>' + content + '</h1>');
        $('#loginModal').modal('hide');
        $('#warning').modal('show');
      }

       function login(){
		          var $loginPhoneNumber = $('#loginPhoneNumber');
          var $pwd = $('#loginPassword');

          if ($loginPhoneNumber.val() == "") {
            warning('登录号码不能为空');
            return;
          }
          if ($loginPhoneNumber.val().length != 11) {
            warning('号码不正确');
            return;
          }

          if ($pwd.val() == "") {
            warning('密码错误');
            return;
          }
          var loginData = {
              'loginPhoneNumber': $loginPhoneNumber.val(),
              'loginPassword': $pwd.val()
            };
          $.ajax({
            url: "{% url 'login:loginVerify' %}",
            //请求的url地址
            type:"post",
            //请求方式
            dataType: "json",
            //返回格式为json
            async: true,
            //请求是否异步，默认为异步，这也是ajax重要特性
            data: JSON.stringify(loginData),
            //参数值
            beforeSend: function() {
              //请求前的处理
            },
            success: function(data) {
              if (data['statusCode'] == "1") //1为电话不存在
              {
                warning('用户不存在');
                return;
              } else if (data['statusCode'] == "2") //2为密码错误
              {
                warning('密码错误');
                return;
              }

              $.cookie('loginStatus', '1', {
                expires: 1,
                path: '/'
              });
              $.cookie('nickName', data['nickName'], {
                expires: 1,
                path: '/'
              });
              $.cookie('phoneNumber', data['phoneNumber'], {
                expires: 1,
                path: '/'
              });
              $.cookie('password', data['pwd'], {
                expires: 1,
                path: '/'
              });

              afterLogin();
              warning(data['nickName']+'登陆成功！！');
            },
            complete: function() {
              //请求完成的处理
            },
            error: function() {
              //请求出错处理
              warning('请求出错');
            }
          })
	};
      
	  
	  
	  function afterLogin()
      {
        $('#loginBefore').addClass('hide');
        $('#userInfoNickName').html('欢迎你：'+$.cookie('nickName'));
        $('#loginAfter').removeClass('hide');
        $('#loginModal').modal('hide');
      };

      function afterUnlogin()
      {
        $('#loginBefore').removeClass('hide');
        $('#userInfoNickName').html('欢迎你：'+$.cookie('nickName'));
        $('#loginAfter').addClass('hide');
      };

      function cookieClear() {
        $.cookie('nickName',null,{path:'/'});
        $.cookie('phoneNumber',null,{path:'/'});
        $.cookie('password',null,{path:'/'});
        $.cookie('loginStatus','0',{expires:1,path:'/'});
      };



