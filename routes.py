from flask import session, request, redirect, url_for, render_template, flash, abort, jsonify
import random
import datetime
import string

from db import db
from models import URL

# Username and password for accessing URL list page
username = "admin"
password = "123456"


def redirect_code(code):
    """
    Endpoint for redirecting to original URL.
    :param code: Code of shortened URL
    :return: Redirection to page, or 404 error if URL does not exist in database
    """

    entry = URL.query.filter_by(shortened_url=code).first()
    if entry:
        return redirect(entry.original_url)
    abort(404)


def new():
    """
    Endpoint for creating a new URL entry in database
    :return: JSON with URL created
    """

    # Register new URL if post data is received
    if request.method == "POST":

        args = request.form.copy()

        # If user provided a desired code, check if it's available
        if "shortened_url" in args:
            if URL.query.filter_by(shortened_url=args['shortened_url']).count() > 0:
                response = jsonify({'error': "Code {0} is already taken.".format(args['shortened_url'])})
                response.status_code = 400
                return response

        # Generate random code if desired short name is not given
        if "shortened_url" not in args:
            while True:

                # Update seed for generation of random numbers
                random.seed()

                # Generate a 5-character random string with letters and numbers
                suggestion = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits)
                                     for _ in range(5))

                # If suggested code doesn't exist in database, accept it
                if URL.query.filter_by(shortened_url=suggestion).count() == 0:
                    break

            args["shortened_url"] = suggestion

        # Set expiration date as 7 days from now, if not specified
        if "expiration_date" not in args:
            expiration_date = datetime.date.today() + datetime.timedelta(days=7)
            args["expiration_date"] = expiration_date.strftime("%Y-%m-%d")

        # Insert URL into table
        new_entry = URL(shortened_url=args["shortened_url"], original_url=args["original_url"],
                        expiration_date=args["expiration_date"])
        db.session.add(new_entry)
        db.session.commit()

        # Return success response
        entry = URL.query.filter_by(shortened_url=args["shortened_url"]).first()
        return jsonify({
            "url": request.base_url.replace('/new', '/') + entry.shortened_url,
            "data": {
                "id": entry.id,
                "shortened_url": entry.shortened_url,
                "original_url": entry.original_url,
                "expiration_date": entry.expiration_date
            }
        })

    # This route exists only for POST requests, so a 404 error is thrown otherwise
    abort(404)


def login():
    """
    Route for authenticating user
    :return: Redirection for main page if user can be authenticated, or to login page otherwise
    """

    # If post data is received, try to authenticate user
    if request.method == "POST":

        # Get user inputs
        form_username = request.form.get('username')
        form_password = request.form.get('password')

        # Check if credentials match
        if form_username != username or form_password != password:
            flash('Invalid credentials.')
            return render_template('login.html')

        # If credentials are correct, create session and redirect to main page
        session['username'] = form_username
        return redirect(url_for('home'))

    # Otherwise, render login page
    return render_template('login.html')


def logout():
    """
    Route for exiting restricted page
    :return: Redirection for main page
    """

    session.pop('username')
    return redirect(url_for('home'))


def home():
    """
    Route for viewing URLs in database
    :return: Home page rendering if user is authenticated, or redirection to login page otherwise
    """

    # If user is not logged in, redirect to login page
    if 'username' not in session:
        return redirect(url_for('login'))

    # Define offset for pagination (default: 0)
    if 'page' not in request.args:
        page = 1
    else:
        try:
            page = int(request.args['page'])
            if page < 1:
                page = 1
        except ValueError:
            page = 1

    # Define limit for pagination (default: 5)
    if 'limit' not in request.args:
        limit = 5
    else:
        try:
            limit = int(request.args['limit'])
        except ValueError:
            limit = 5

    # Total count in database
    total = len(URL.query.all())

    # Query data to be returned
    entries = URL.query.limit(limit).offset((page - 1) * limit).all()
    data = []
    for entry in entries:
        data.append({
            "id": entry.id,
            "shortened_url": entry.shortened_url,
            "original_url": entry.original_url,
            "expiration_date": entry.expiration_date,
        })

    # Evaluate number of pages
    last = total // limit
    if total % limit > 0:
        last += 1

    # Pagination data
    link = '{0}?page={1}&limit={2}'
    links = {
        'self': link.format(request.base_url, page, limit),
        'first': link.format(request.base_url, '1', limit),
        'last': link.format(request.base_url, last, limit)
    }
    if page > 1:
        links['prev'] = link.format(request.base_url, page - 1, limit)
    if page < last:
        links['next'] = link.format(request.base_url, page + 1, limit)

    # Load home page
    return render_template('home.html', data={'_links': links, 'data': data, 'current': page, 'last': last})
