from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,IntegerField
from wtforms.validators import DataRequired,Length
from flask_wtf.file import FileRequired,FileField,FileAllowed

class Register(FlaskForm):
    username=StringField(validators=[DataRequired("用户名为空！")],description="用户名")
    password=PasswordField(validators=[DataRequired("密码为空！")])
    name=StringField(validators=[DataRequired("姓名为空！")])
    idnum=StringField(validators=[DataRequired(),Length(18,18,"身份证号码的长度为18")],description="身份证号")
    submit=SubmitField('确认')

class Login(FlaskForm):
    username = StringField(validators=[DataRequired("用户名为空！")], description="用户名")
    password = PasswordField(validators=[DataRequired("密码为空！")])
    submit = SubmitField('登录')

class Upload(FlaskForm):
    image=FileField('上传头像',validators=[FileRequired(),FileAllowed(['jpg'])])
    submit=SubmitField('上传头像')

class Download(FlaskForm):
    username = StringField(validators=[DataRequired("用户名为空！")], description="用户名")
    submit=SubmitField('下载头像')

class Leave(FlaskForm):
    message=StringField(validators=[DataRequired("765")])
    submit=SubmitField('留言')

class DelUser(FlaskForm):
    username=StringField(validators=[DataRequired("")])
    submit=SubmitField('删除用户')

class Restore(FlaskForm):
    username = StringField(validators=[DataRequired("")])
    submit = SubmitField('还原头像')

class DelMessage(FlaskForm):
    id=IntegerField(validators=[DataRequired("")])
    submit=SubmitField('删除留言')

class Xss(FlaskForm):
    input=StringField(validators=[DataRequired("")])
    submit=SubmitField('输入')
