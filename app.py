from typing import Any

from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)
file_path = 'data/blogs.json'
posts_dict: dict[Any, Any] = {}

def create_post_dict():
    """
    Creates a Global Dictionary of Dictionaries from posts.
    Using a Dictionary of Dictionaries makes handling of posts easier
    and faster, specially when we have to deal with a big number
    of posts.
    """
    posts = load_posts()
    for post in posts:
        try:
            posts_dict[post['id']] = {"id": post["id"],
                                      "author": post["author"],
                                      "title": post["title"],
                                      "content": post["content"],
                                      "likes": post["likes"]
                                      }
        except KeyError as e:
            print(f"Post {post['id']} not loaded because of error on {e}. "
                  f"Please check {file_path}")


def load_posts():
    """
    loads blog posts from JSON
    """
    try:
        with open(file_path, "r") as json_file:
            blog_posts = json.load(json_file)
    except FileNotFoundError:   # If the file doesn't exist...
        blog_posts = []         # ...start with an empty blog.
    return blog_posts


def save_posts():
    """
    Creates the posts list, from the values of the posts dictionary
    and saves it as JSON file.
    """
    posts = list(posts_dict.values())
    with open(file_path, "w") as json_file:
        json.dump(posts, json_file, indent=4)


def fetch_post_by_id(post_id):
    """
    Checks if a post_id exists in the posts dictionary and if it exists,
    returns the post by this id.
    :param post_id: the post id
    :return: post by post_id (or None if post_id does not exist)
    """
    if post_id in posts_dict:
        return posts_dict[post_id]


@app.route('/')
def index():
    """
    Renders to html all blog posts (taken from the values of the
    posts Dictionary)
    """
    return render_template('index.html',
                           posts=posts_dict.values())


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handles adding a new blog post.
    GET: Displays the form for adding a post
    POST: Saves the new post and redirects to the homepage
    """
    if request.method == 'POST':
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")
        if posts_dict == {}:
            id = 1
        else:
            id = max(posts_dict.keys()) + 1
        posts_dict[id] = {
            "id": id,
            "author": author,
            "title": title,
            "content": content,
            "likes": 0
        }
        save_posts()
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Handles updating a blog post.
    GET: Displays the form for updating the post
    POST: Saves the updated post and redirects to the homepage
    :param post_id: the id of the post to be updated
    :return: depending on the method used, the form for updating the
        post, or redirects to the homepage,
        or 404 if the post to be updated is not found.
    """
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")
        likes = posts_dict[post_id].get("likes")
        posts_dict[post_id] = {
            "id": post_id,
            "author": author,
            "title": title,
            "content": content,
            "likes": likes
        }
        save_posts()
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """
    removes a blog post by ID,
    updates the JSON file and redirects to the homepage,
    (or 404 if the post to be deleted is not found).
    """
    post = fetch_post_by_id(post_id)
    if post is None: # Post not found
        return "Post not found", 404
    del posts_dict[post_id]
    save_posts()
    return redirect(url_for('index'))


@app.route('/like/<int:post_id>')
def like(post_id):
    """
    increases the like count of a blog post
    """
    post = fetch_post_by_id(post_id)
    if post is None:  # Post not found
        return "Post not found", 404
    posts_dict[post_id]["likes"] += 1
    save_posts()
    return redirect(url_for('index'))


if __name__ == '__main__':
    create_post_dict()
    app.run(host="0.0.0.0", port=5000, debug=True)
