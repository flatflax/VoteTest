# mysite #

根据Django的[官方教程](https://docs.djangoproject.com/en/2.0/intro/)，使用Django开发一个投票网站，并由此学习Django的基本使用。


## 创建project和app ##

创建project名为mysite，创建polls。一个project下可以有多个app，一个app也可以归属于多个project，它们是多对多关系。
    
    django-admin.py startproject mysite
	cd path\to\mysite
	python manage.py startapp polls

创建完成后，将polls添加到`setting.py`的`INSTALLED_APPS`下。

创建后的项目目录如下：

	mysite/
	    manage.py
	    mysite/
	    	__init__.py
	    	settings.py
	    	urls.py
	    	wsgi.py
		polls/
			__init__.py
			admin.py
			migrations/
				__init__.py
			models.py
			tests.py
			urls.py
			views.py

对目录中的部分文件的功能简要介绍如下：

`manage.py` 与Django交互的工具。使用 python manage.py可以查看可以调用的方法。

`settings.py` 配置文件，包括app的配置、数据库的配置等。

`urls.py` 将不同的url映射到不同的view上

`wsgi.py` WSGI是web server gateway interface，这个文件是使project符合这种协议的入口点（entry-point）

`admin.py` Django自带的一个管理界面，可以注册model在界面中管理

`migrations` 数据库的移行。执行`python manage.py makemigrations` 后会自动生成一个文件在这里。

`models.py` 定义model类

`tests.py` 测试代码

`views.py`映射urls.py里面的url的时候，在views.py里面查找对应的处理方法

对于创建完成的工程，可以运行Django自带的开发服务器 `python manage.py runserver 8080` 查看效果。

## 创建model类（数据库） ##

在models.py中创建继承models.Model的类，对应一个表。表内的字段对应类中的参数。

`def __str__(self)` 用于决定访问admin时的效果。在python2时，则改为` __unicode__`

创建好的数据库表，执行`python manage.py makemigrations polls`
创建移行。执行`python manage.py migrate`将变化应用到数据库。

    python manage.py makemigrations polls
	python manage.py sqlmigrate polls 0001
	python manage.py migrate

## admin管理 ##

修改admin.py，将数据库交给admin后台管理。

`python manage.py createsuperuser` 创建超级用户，然后填写相应的用户名，邮箱和密码。

    from .models import Question
	admin.site.register(Question)

上述代码将先前创建的数据库表(Question(model类))在admin上注册。


## 结合template修改view ##
view的作用有两个，一个是返回`HttpResponse`，其中包含着响应页面所需的信息；另一个是抛出错误，例如404。

view可以通过django或者其他第三方的Template系统读取数据库的信息，或者读取一些现存的文档。

由于在view中修改页面设计过于繁杂，因此选择结合template和view来修改页面显示和设计。

预设的project中，我们可以从`setting.py`的`TEMPLATES`配置中看到Django是如何加载和应用template的。`'APP_DIRS': True`，这说明预设的Django project配置了一个template后端(？)。DjangoTemplates会在每一个`INSTALLED_APPS`中寻找一个templates子目录。

在编写view时，也可以使用`return render(request, <url>, content)`来作为`reutrn HttpResponse(template.render(content, request))`的简化版。

**移除hardcoded**：在页面跳转的时候，为了使链接是动态的，可以在template中将跳转连接改为下例样式。
	
	{% url 'detail' question.id %}
	{% url %} 调用urls.py中设置好的url

## 表单form ##
对`radio input`组件，使用`{{ forloop.counter }}`生成一个choiceid。

对提交的表单设`<form action="{% url 'polls:vote' question.id %}" method="post">`，对view中的vote方法作POST。

在vote方法中，使用try-catch对choice.vote加一，如果失败或提交的表单为空，则重新渲染`detail.html`,要求用户重新投票。如果投票处理成功，则重定向到`result.html`。

**注** ：需要注意的是，每次处理上述POST请求成功的时候，都应该返回一个HttpResponseRedirect。这样可以避免当用户点击浏览器的返回键时，不会重新发出一次POST请求。

## 使用CSS ##

首先确保`settings.py`中`INSTALLED_APPS`中已包含`'django.contrib.staticfiles'`，以及

    STATIC_URL = '/static/'

在生产环境中，需要在`urls.py`中添加

    urlpatterns = [
    # ... the rest of your URLconf goes here ...
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
具体参考[该链接](https://docs.djangoproject.com/en/dev/howto/static-files/deployment/)


## 用户登录 ##
[参考](https://docs.djangoproject.com/en/2.0/topics/auth/default/#topic-authorization)

### CSRF token missing or incorrect.

跨域访问相关

1. 确认`'django.middleware.csrf.CsrfViewMiddleware'`存在于工程`settings.py`中的`MIDDLEWARE`。
2. 在html的form中添加模板标签`{% csrf_token %}`
3. `views.py`中的`render()`使用`RequestContext`

## 后台修改密码 ##

	python manage.py shell
	>>from django.contrib.auth.models import User
	>>user = User.objects.filter(is_superuser=True)	
	# 获取超级管理员
	# print可以获取username
	>>user = User.objects.get(username='admin')
	>>user.set_password("new_password")
	>>user.save

## 用户注册 ##

*　创建一个`class UserForm(forms.Form)`类，用于和表单对应。
* 可以使用django自带的user类`from django.contrib.auth.models import User`，也可以使用自己创建的user表。实例化一个新的user对象。
* 将请求中表单信息装入`UserForm`,然后将`UserForm`获取的信息装入`User.objects.create_user()`中。
* `user.save`保存，作跳转。

## 确认用户登陆状态 ##

`user.is_authenticated()`在template和view中都可以使用。

## 分页 ##

[参考文档地址](https://docs.djangoproject.com/en/2.1/topics/pagination/)

`from django.core.paginator import Paginator`