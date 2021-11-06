import json

from flask import render_template
from flask_login import login_required
import pandas as pd
import plotly.express as px
import plotly

from app import db
from app.chart import bp
from app.models import Book

@bp.route('/')
@login_required
def chart_list():
    return render_template('chart_list.html', title = 'List of Charts')

@bp.route('/book_ratings')
@login_required
def book_ratings_chart():
    # Retrieve all the books in the collection
    book_query = Book.query
    df = pd.read_sql(book_query.statement, book_query.session.bind)

    # Draw the chart and dump it into JSON format
    chart = px.bar(df, x='title', y='critics_rating')
    chart_JSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder, indent=4)

    # Returns the template, including the JSON data for the chart
    return render_template('chart_page.html', title = 'Critic ratings for books', chart_JSON = chart_JSON)
    
@bp.route('/user_books')
@login_required
def user_books_chart():
    # Run query to get count of books owned per user and load into DataFrame
    query = (
        "SELECT username, count(*) as books_owned "
        "FROM user_book ub "
        "JOIN user u on ub.user_id = u.id "
        "GROUP BY username"
    )
    df = pd.read_sql(query, db.session.bind)

    # Draw the chart and dump it into JSON format
    chart = px.bar(df, x ='username', y='books_owned')
    chart_JSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder, indent=4)

    # Returns the template, including the JSON data for the chart
    return render_template('chart_page.html', title = 'Books owned per user', chart_JSON = chart_JSON)

# route for a bar chart that compares books read per year by user
@bp.route('/books_per_year')
@login_required
def books_per_year_chart():
# Run query to get count of books of each genre and load into DataFrame
    query = (
        "SELECT username, books_read_per_year from user"
    )
    df = pd.read_sql(query, db.session.bind)

    # Draw the chart and dump it into JSON format
    chart = px.bar(df, x ='username', y='books_read_per_year', 
    color='username', labels={'books_read_per_year': 'Books read', 'username': 'Name of User'})
    chart_JSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder, indent=4)

    # Returns the template, including the JSON data for the chart
    return render_template('chart_page.html', title = 'Books read per year', chart_JSON = chart_JSON)

# oute for a bar chart that compares number of books per genre
@bp.route('/genre_books')
@login_required
def genre_books_chart():
# Run query to get count of books of each genre and load into DataFrame
    query = (
        "SELECT name, count(genre_id) as genre_count from book "
        "INNER JOIN genre ON book.genre_id=genre.id "
        "GROUP BY genre.name;"
    )
    df = pd.read_sql(query, db.session.bind)

    # Draw the chart and dump it into JSON format
    chart = px.bar(df, x ='name', y='genre_count',
    color='name', labels={'name': "Genre", 'genre_count': 'Number of Books'})
    chart_JSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder, indent=4)

    # Returns the template, including the JSON data for the chart
    return render_template('chart_page.html', title = 'Books by genre', chart_JSON = chart_JSON)