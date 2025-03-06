from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)
file_path = 'blogs.json'

def load_posts():
    with open(file_path, "r") as json_file:
        blog_posts = json.loads(json_file.read())
    json_file.close()
    return blog_posts

def save_posts(posts):
    with open(file_path, "w") as json_file:
        json.dump(posts, json_file)
    json_file.close()

@app.route('/')
def index():
    return render_template('index.html', posts=load_posts())


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")
        blog_posts = load_posts()
        id = blog_posts[-1]["id"] + 1
        blog_posts.append({"id": id, "author": author, "title": title, "content": content})
        save_posts(blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = load_posts()
    for post in blog_posts:
        if post["id"] == post_id:
            blog_posts.remove(post)
            save_posts(blog_posts)
            return redirect(url_for('index'))
    # Find the blog post with the given id and remove it from the list
    # Redirect back to the home page



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)