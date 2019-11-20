from flask import jsonify, request, render_template
from app.forms.search import searchForm
from app.libs.department import Department
from app.models.search import SearchView
from app.web import web

@web.route('/search')
def search():
    form = searchForm(request.args)
    searchObj = SearchView(form)
    list = Department(searchObj).itemsList
    if form.validate():
        return render_template('txtList.html',data = list)
        # return Department(searchObj).__dict__
    else:
        return jsonify({'msg':'参数未经过验证'})

