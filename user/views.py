import logging
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt    # 取消csrf
from . import forms
from . import models

logger = logging.getLogger('user')
# Create your views here.


@csrf_exempt
def index(request):
    logger.info('request session: %s', request.session.items())
    title = '首页'
    logger.info('got local vars: %s', locals())
    return render(request, 'index.html', locals())


@csrf_exempt
def login(request):
    logger.info('request session: %s', request.session.items())
    title = '登录'
    error = ''
    login_form = forms.LoginForm()

    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        is_valid = login_form.is_valid()
        logger.info('POST login form is valid: %s', is_valid)
        if is_valid:  # 判断是否填写完成，如果 clean 方法报 attribute error 则为 false
            user = login_form.cleaned_data  # 获取表单提交数据
            logger.info('got user: %s', user)
            user_info = models.User.objects.get(username=user['username'])
            request.session['is_login'] = True
            request.session['username'] = user['username']
            request.session['school_name'] = ''
            request.session['province'] = user_info.province
            request.session['student_type'] = user_info.subject
            request.session['epoch'] = '本科批'
            return redirect('/')
        else:
            # 获取全局的error信
            # 息,只显示第一个
            errors = login_form.errors.get('__all__')
            logger.info('got error count: %s', len(errors))
            if len(errors) != 0:
                error = errors[0]

    logger.info('got local vars: %s', locals())
    return render(request, 'login.html', locals())


@csrf_exempt
def register(request):
    logger.info('request session: %s', request.session.items())
    title = '注册'
    error = ''
    register_form = forms.RegisterForm()
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)  # 为什么要传 request.POST
        if register_form.is_valid():    # 判断是否填写完成
            user = register_form.cleaned_data  # 清理数据
            models.User.objects.create(username=user['username'], password=user['password1'])
            return redirect('/login/')
        else:
            # 获取全局的error信息,只显示第一个
            errors = register_form.errors.get('__all__')
            logger.info('got error count: %s', len(errors))
            if len(errors) != 0:
                error = errors[0]

    return render(request, 'register.html', locals())


@csrf_exempt
def logout(request):
    logger.info('request session: %s', request.session.items())
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        logger.info('request session is not logged in, no need to flush')
        return redirect("/")

    # flush 清除 session 并跳转到主页
    request.session.flush()
    return redirect("/")


@csrf_exempt
def student_info(request):
    logger.info('request session: %s', request.session.items())
    title = '个人信息'
    if not request.session.get('is_login'):
        # 如果本来就未登录，也就没有信息一说，跳去登录界面
        return redirect("/login/")

    username = request.session.get('username')
    user = models.User.objects.get(username=username)
    logger.info('got user: %s', user.__dict__)
    if request.method == 'GET':
        student_form = forms.StudentInfoForm(initial={
            'sex': user.sex,
            'province': user.province,
            'subject': user.subject,
            'score': user.score,
        })
    if request.method == 'POST':
        student_form = forms.StudentInfoForm(request.POST)
        if student_form.is_valid():  # 判断是否填写完成
            user.sex = student_form.cleaned_data['sex']
            user.province = student_form.cleaned_data['province']
            user.subject = student_form.cleaned_data['subject']
            user.score = student_form.cleaned_data['score']
            user.save()
            message = '修改成功'
            request.session['student_type'] = student_form.cleaned_data['subject']

    logger.info('got local vars: %s', locals())
    return render(request, 'student_info.html', locals())
