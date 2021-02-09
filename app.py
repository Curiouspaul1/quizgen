from flask import Flask, render_template, url_for, request, session
from faunadb import query as q
from faunadb.client import FaunaClient
from dotenv import load_dotenv
import os

load_dotenv() # loads env variables from .env files

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('secret')
client = FaunaClient(secret=os.getenv('FAUNA_KEY'))
_vars = {
    'category_name': None,
    'after':None,
    'before':None
}

# routes
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/addquiz", methods=['POST'])
def add_quiz():
    _data = request.form
    # search for category specified using index
    get_category = client.query(q.get(q.match(q.index('category_by_name'), _data['category'])))
    new_quiz = client.query(
        q.create(q.collection('Quiz'), {
            "data":{
                "quiz_body":_data['quiz-body'],
                "A": _data["A"],
                "B": _data["B"],
                "C": _data["C"],
                "D": _data["D"],
                "answer": _data["ans"],
                "category": get_category['data']['name']
            }
        })
    )

    return {
        "status":"sent"
    }, 200

@app.route("/quizbycategory", defaults={'category':None}, methods=['POST'])
@app.route("/quizbycategory/<category>")
def get_quiz_by_category(category):
    if request.method == 'GET':
        # get categoruy
        get_category = client.query(q.get(q.match(q.index('category_by_name'), category)))
        query = client.query(
            q.map_(
                lambda var: q.get(var),
                q.paginate(
                    q.match(
                        q.index("quiz_by_category"),
                        get_category['data']['name']
                    ),
                    size=3
                )
            )
        )
        result = [i['data'] for i in query['data']]
        _vars['category_name'] = category
        if 'after' in query.keys():
            _vars['after'] = query['after'][0]
        #print(_vars)
        print(query)
        return render_template('quizpage.html', result=result)
    elif request.method == 'POST':
        if 'next' in request.form.keys():
            get_category = client.query(q.get(q.match(q.index('category_by_name'), _vars['category_name'])))
            query = client.query(
                q.map_(
                    lambda var: q.get(var),
                    q.paginate(
                        q.match(
                            q.index("quiz_by_category"),
                            get_category['data']['name']
                        ),
                        size=3,
                        after=_vars['after']
                    )
                )
            )
            result = [i['data'] for i in query['data']]
            if 'before' in query.keys():
                _vars['before'] = query['before'][0]
            if 'after' in query.keys():
                _vars['after'] = query['after'][0]
            return render_template('quizpage.html', result=result)
        if 'prev' in request.form.keys():
            #print(_vars)
            get_category = client.query(q.get(q.match(q.index('category_by_name'), _vars['category_name'])))
            query = client.query(
                q.map_(
                    lambda var: q.get(var),
                    q.paginate(
                        q.match(
                            q.index("quiz_by_category"),
                            get_category['data']['name']
                        ),
                        size=3,
                        before=_vars['before']
                    )
                )
            )
            result = [i['data'] for i in query['data']]
            if 'after' in query.keys():
                _vars['after'] = query['after'][0]
            if 'before' in query.keys():
                _vars['before'] = query['before'][0]
            return render_template('quizpage.html', result=result)

if __name__ == "__main__":
    app.run(debug=True)
