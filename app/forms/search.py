
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length

class searchForm(Form):
    siteName = StringField(validators=[Length(min=0,max=50)], default='海淀区信息公开大厅')
    department = StringField(validators=[Length(min=0)], default='')
    column = StringField(validators=[Length(min=0,max=100)], default='')
    keyword = StringField(validators=[Length(min=0,max=200)])
    startTime = StringField(validators=[Length(min=0,max=50)], default='')
    endTime = StringField(validators=[Length(min=0, max=50)], default='')
