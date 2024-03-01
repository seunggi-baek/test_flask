# 생활코딩 강의 샘플 : https://www.youtube.com/watch?v=X_n6IZmieV8&list=PLuHgQVnccGMClNOIuT3b3M4YZjxmult2y

# Flask에서 라우팅은 사용자가 웹 애플리케이션에서 특정 URL을 요청했을 때 해당 요청을 처리하는 메커니즘을 말합니다. 
# 간단히 말해, 어떤 URL이 어떤 함수와 연결되는지를 정의하는 것이라고 볼 수 있습니다.

from flask import Flask, request, redirect

app = Flask(__name__)

nextId = 4
# Dictionary
topics = [
    {'id': 1, 'title': 'html', 'body': 'html is...'},
    {'id': 2, 'title': 'css', 'body': 'css is...'},
    {'id': 3, 'title': 'javascript', 'body': 'javascript is...'},
]

def template(contents, content, id=None):
    contextUI = ''
    if id != None:
        contextUI = f'''
            <li><a href="/update/{id}">update</a></li>
            <li><form action="/delete/{id}" method="POST"><input type="submit" value="delete" /></form></li>
        '''
    return f'''
        <!doctype html>
        <html>
            <body>
                <h1><a href="/">WEB</a></h1>
                <ol>
                    {contents}
                </ol>
                {content}
                <ul>
                    <li><a href="/create">create</a></li>
                    {contextUI}
                </ul>
            </body>
        </html>
    '''
    
def getContents():
    liTags = ''
    for topic in topics:
        liTags = liTags + f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return liTags
    

#  @app.route() 데코레이터를 사용하여 특정 URL에 대한 처리 함수를 정의합니다.
# ''' 를 쓰면 멀티라인 작성이 가능합니다.
@app.route('/')
def index():
    return template(getContents(), "<h2>Welcome</h2>Hello, Web")

# <id>은 동적인 부분으로, 사용자가 브라우저에서 '/read/id'과 같은 URL을 요청하면 
# 해당 id를 보여주는 함수가 실행됩니다.
@app.route('/read/<int:id>')
def read(id):
    title = ''
    body = ''
    for topic in topics:
        if id == topic['id']: 
            title = topic['title']
            body = topic['body']

    return template(getContents(), f'<h2>{title}</h2>{body}', id)

# form 전송방식 (GET (기본), POST)
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "GET":
        content = '''
            <form action="/create" method="POST">
                <p><input type="text" name="title" placeholder="title" /></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit" value="create"/></p>
            </form>
        '''
        return template(getContents(), content)
    elif request.method == "POST":
        global nextId
        title = request.form['title']
        body = request.form['body']
        newTopic = {'id': nextId, 'title': title, 'body': body}
        topics.append(newTopic)
        url = f'/read/{nextId}'
        nextId += 1
        return redirect(url)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == "GET":
        title = ''
        body = ''
        for topic in topics:
            if id == topic['id']: 
                title = topic['title']
                body = topic['body']
                
        content = f'''
            <form action="/update/{id}" method="POST">
                <p><input type="text" name="title" placeholder="title" value={title} /></p>
                <p><textarea name="body" placeholder="body">{body}</textarea></p>
                <p><input type="submit" value="update"/></p>
            </form>
        '''
        return template(getContents(), content)
    elif request.method == "POST":
        global nextId
        title = request.form['title']
        body = request.form['body']
        for topic in topics:
            if id == topic['id']:
                topic['title'] = title
                topic['body'] = body
                break
        url = f'/read/{nextId}'
        return redirect(url)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    for topic in topics:
        if id == topic['id']:
            topics.remove(topic)
            break
    return redirect('/')
   
    
if __name__ == '__main__':
    # debug=True 로 설정해놓으면 소스 수정 후 저장하면 자동으로 서버 재시작
    app.run(debug=True)