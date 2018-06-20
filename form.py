import wtforms
from wtforms import validators

class CreateForm(wtforms.Form):
    username = wtforms.StringField(validators=[validators.InputRequired(message=u'请输入用户名')])
    email = wtforms.StringField(validators=[validators.length(min=6, max=30)])
    password = wtforms.StringField(validators=[validators.InputRequired()])
    check_password = wtforms.StringField(validators=[validators.InputRequired(),validators.EqualTo('password', message='两次输入的密码不匹配')])

