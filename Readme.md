# VoteTest #

根据Django的[官方教程](https://docs.djangoproject.com/en/2.0/intro/)，使用Django开发一个投票网站，并由此学习Django的基本使用。

学习笔记[详见](https://flatflax.gitbooks.io/web_study/content/)

## 目前实现的功能 ##

* 初始化Model
* admin管理投票题目和可选项，增删
* 首页显示所有可投票题目
* `/<question_id>` 显示投票内容
* id页发出POST请求,提交表单至`/<question_id>/vote`
* 提交成功后重定向至`/<question_id>/result`

## Todo List ##

* ~~前端美化~~
* 用户登陆
* ……
