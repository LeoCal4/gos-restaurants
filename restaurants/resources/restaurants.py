from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
# from flask_login import current_user, login_required
from restaurants.dao.like_manager import LikeManager
from restaurants.dao.restaurant_availability_manager import \
    RestaurantAvailabilityManager
from restaurants.dao.restaurant_manager import RestaurantManager
from restaurants.dao.restaurant_rating_manager import RestaurantRatingManager
from restaurants.dao.table_manager import TableManager
from restaurants.forms.add_measure import MeasureForm
from restaurants.forms.add_stay_time import StayTimeForm
from restaurants.forms.add_table import TableForm
from restaurants.forms.add_times import TimesForm
from restaurants.forms.restaurant import RestaurantForm
from restaurants.models.restaurant import Restaurant, geolocator
from restaurants.models.restaurant_availability import RestaurantAvailability
from restaurants.models.restaurant_rating import RestaurantRating
from restaurants.models.table import Table


restaurants = Blueprint('restaurants', __name__)


def my_restaurant():
    """Given the operator id, this method allows him to see the details of his restaurant
        Linked to route /my_restaurant [POST]
    Returns:
        Redirects to the restaurants details method, or a failed response if the user_id is invalid
    """
    user_id = request.form['user_id']
    if user_id is None:
        return {}, 400
    return details(user_id)


def restaurant_sheet(restaurant_id):
    """This method returns a single restaurant
        Linked to route /restaurants/{restaurant_id} [GET]
    Args:
        restaurant_id (int): univocal identifier of the restaurant
    Returns: 
        Invalid request if the restaurant does not exists
        A json specifying the info needed to render the restaurant page otherwise
    """
    restaurant = RestaurantManager.retrieve_by_id(id_=restaurant_id)

    if restaurant is None:
        return {}, 400

    list_measure = restaurant.measures.split(',')[1:]
    average_rate = RestaurantRatingManager.calculate_average_rate(restaurant)

    return {'restaurant': restaurant, 'list_measures': list_measure, 
            'average_rate': average_rate, 'max_rate': RestaurantRating.MAX_VALUE}, 200


def like_toggle(restaurant_id):
    """Updates the like count
        Linked ot /restaurants/like/<restaurant_id> [POST]
    Args:
        restaurant_id (int): univocal identifier of the restaurant

    Returns:
        Redirects to the single page for a restaurant
    """
    user_id = request.form['user_id']
    if user_id is None:
        return {}, 400
    # TODO: check if restaurant_id is valid

    toggle_like(user_id, restaurant_id)

    # TODO: should resources now redirect to other resources' methods or should 
    #they just return their own messages and statuses?
    return restaurant_sheet(restaurant_id)


def get_add(id_op):
    """Given an operator, this method returns the form used to add a restaurant
        Linked to /restaurants/add/<id_op> [get]
    Args:
        id_op (int): univocal identifier for the customer

    Returns: 
        The form to load in the page
    """
    form = RestaurantForm()
    return {'form': form}, 200


# @restaurants.route('/restaurants/add/<int:id_op>', methods=['GET', 'POST'])
# @login_required
def post_add(id_op):
    """Given an operator, this method allows him to add a restaurant
        Linked to /restaurants/add/<id_op> [POST]
    Args:
        id_op (int): univocal identifier for the customer

    Returns:
        Invalid response if the request method or the form are not correct 
        Confirms the creation of the restaurant otherwise
    """
    form = RestaurantForm()
    if form.validate_on_submit():
        name = form.data['name']
        address = form.data['address']
        city = form.data['city']
        phone = form.data['phone']
        menu_type = form.data['menu_type']
        location = geolocator.geocode(address+" "+city)
        lat = 0
        lon = 0
        if location is not None:
            lat = location.latitude
            lon = location.longitude
        restaurant = Restaurant(name, address, city, lat, lon, phone, menu_type)
        restaurant.owner_id = id_op

        RestaurantManager.create_restaurant(restaurant)

        # return redirect(url_for('auth.operator', id=id_op))
        return {'message': 'Restaurant succesfully added'}, 200
    return {}, 400
    # return render_template('create_restaurant.html', form=form)


# @restaurants.route('/restaurants/details/<int:id_op>', methods=['GET', 'POST'])
# @login_required
def details(id_op):
    """Given an operator, this method allows him to see the details of his restaurant
        Linked to /restaurants/details/<id_op> [GET]
    Args:
        id_op (int): univocal identifier of the operator

    Returns:
        Returns the page of the restaurant's details
    """
    table_form = TableForm()
    time_form = TimesForm()
    measure_form = MeasureForm()
    avg_time_form = StayTimeForm()
    restaurant = RestaurantManager.retrieve_by_operator_id(id_op)

    if restaurant is None:
        # TODO: change or keep it?
        return get_add(id_op)
    list_measure = restaurant.measures.split(',')[1:]
    tables = TableManager.retrieve_by_restaurant_id(restaurant.id)
    ava = restaurant.availabilities
    avg_stay = restaurant.avg_stay

    avg_stay = convert_avg_stay_format(avg_stay)

    return {'restaurant': restaurant, 'tables': tables, 'table_form': table_form,
            'time_form': time_form, 'times': ava, 'measure_form': measure_form, 
            'avg_time_form': avg_time_form, 'avg_stay': avg_stay, 'list_measure': list_measure}, 200
    # return render_template('add_restaurant_details.html',
    #                        restaurant=restaurant, tables=tables,
    #                        table_form=table_form, time_form=time_form,
    #                        times=ava, measure_form=measure_form, avg_time_form=avg_time_form,
    #                        avg_stay=avg_stay,
    #                        list_measure=list_measure[1:])


# @restaurants.route('/restaurants/save/<int:id_op>/<int:rest_id>', methods=['GET', 'POST'])
# @login_required
def add_tables(id_op, rest_id):
    """This method gives the operator the possibility to add tables to his restaurant
        Linked to /restaurants/save_tables/<id_op>/<rest_id> [POST]
    Args:
        id_op (int): univocal identifier of the operator
        rest_id (int): univocal identifier of the restaurant

    Returns:
        Invalid request if the tables data are not valid
        Tables successfully added otherwise
    """
    table_form = TableForm()
    restaurant = RestaurantManager.retrieve_by_operator_id(id_op)

    if table_form.is_submitted():
        num_tables = table_form.data['number']
        capacity = table_form.data['max_capacity']
        try:
            for _ in range(0, num_tables):
                table = Table(capacity=capacity, restaurant=restaurant)
                TableManager.create_table(table)
        except ValueError:
            return {'message': 'ValueError'}, 400

    return {'message': 'Tables successfully added'}, 200
    # return redirect(url_for('restaurants.details', id_op=id_op))


# @restaurants.route('/restaurants/savetime/<int:id_op>/<int:rest_id>', methods=['GET', 'POST'])
# @login_required
def add_time(id_op, rest_id):
    """This method gives the operator the possibility to add opening hours to his restaurant
        Linked to /restaurants/save_time/<int:id_op>/<int:rest_id> [POST]
    Args:
        id_op (int): univocal identifier of the operator
        rest_id (int): univocal identifier of the restaurant

    Returns:

    """
    time_form = TimesForm()
    restaurant = RestaurantManager.retrieve_by_id(rest_id)
    availabilities = restaurant.availabilities
    present = False
    if time_form.is_submitted():
        day = time_form.data['day']
        start_time = time_form.data['start_time']
        end_time = time_form.data['end_time']
        if validate_ava(restaurant, day, start_time, end_time):
            flash('Opening Hours updated')
        else:
            flash('Error during opening hours updating')
    return redirect(url_for('restaurants.details', id_op=id_op))

def validate_ava(restaurant, availabilities, day, start_time, end_time):
    """This method validates the restaurant opening hours 

    Args:
        restaurant (restaurant): the actual restaurant
        availabilities (Availabilities): already present restaurant opening hours
        day (String):
        start_time (time): opening hour
        end_time (time): closing hour

    Returns:
        Boolean: True if the opening hours has been added correctly otherwise returns false 
    """
    present = False
    if end_time > start_time:
        for ava in availabilities:
            if ava.day == day:
                ava.set_times(start_time, end_time)
                RestaurantAvailabilityManager.update_availability(ava)
                present = True
        if not present:
            time = RestaurantAvailability(rest_id, day, start_time, end_time)
            RestaurantAvailabilityManager.create_availability(time)
        return True
    else:
        return False

@restaurants.route('/restaurants/savemeasure/<int:id_op>/<int:rest_id>', methods=['GET', 'POST'])
# @login_required
def save_measure(id_op, rest_id):
    """This method gives the operator the possibility to add precaution meausures 
    to his restaurant

    Args:
        id_op (int): univocal identifier of the operator
        rest_id (int): univocal identifier of the restaurant

    Returns:
        Returns the page of the restaurant's details
    """
    measure_form = MeasureForm()
    restaurant = RestaurantManager.retrieve_by_operator_id(id_op)

    if request.method == "POST":
        if measure_form.is_submitted():
            list_measure = restaurant.measures.split(',')
            measure = measure_form.data['measure']
            if measure not in list_measure:
                list_measure.append(measure)
            string = ','.join(list_measure)
            restaurant.set_measures(string)
            RestaurantManager.update_restaurant(restaurant)

    return redirect(url_for('restaurants.details', id_op=id_op))


@restaurants.route('/restaurants/avgstay/<int:id_op>/<int:rest_id>', methods=['GET', 'POST'])
# @login_required
def save_avg_stay(id_op, rest_id):
    avg_time_form = StayTimeForm()
    restaurant = RestaurantManager.retrieve_by_operator_id(id_op)

    if request.method == "POST":
        if avg_time_form.validate_on_submit():
            hours = avg_time_form.data['hours']
            minute = avg_time_form.data['minutes']
            minute = (hours * 60) + minute
            restaurant.set_avg_stay(minute)
            RestaurantManager.update_restaurant(restaurant)
        else:
            flash("Insert positive values")

    return redirect(url_for('restaurants.details', id_op=id_op))


@restaurants.route('/edit_restaurant/<int:id_op>/<int:rest_id>', methods=['GET', 'POST'])
# @login_required
def edit_restaurant(id_op, rest_id):
    """This method allows the operator to edit the information about his restaurant

    Args:
        id_op (int): univocal identifier of the operator
        rest_id (int): univocal identifier of the restaurant

    Returns:
        Returns the page of the restaurant's details
    """
    form = RestaurantForm()
    restaurant = RestaurantManager.retrieve_by_id(rest_id)

    if request.method == "POST":
        if form.is_submitted():
            name = form.data['name']
            restaurant.set_name(name)
            address = form.data['address']
            restaurant.set_address(address)
            city = form.data['city']
            restaurant.set_city(city)
            phone = form.data['phone']
            restaurant.set_phone(phone)
            menu_type = form.data['menu_type']
            restaurant.set_menu_type(menu_type)

            RestaurantManager.update_restaurant(restaurant)
            return redirect(url_for('auth.operator', id=id_op))

    return render_template('update_restaurant.html', form=form)


##### Helper methods #####

def toggle_like(user_id, restaurant_id):
    if LikeManager.like_exists(user_id, restaurant_id):
        LikeManager.delete_like(user_id, restaurant_id)
    else:
        LikeManager.create_like(user_id, restaurant_id)


def convert_avg_stay_format(avg_stay):
    if avg_stay is not None:
        h_avg_stay = avg_stay // 60
        m_avg_stay = avg_stay - (h_avg_stay * 60)
        avg_stay = "%dH:%dM" % (h_avg_stay, m_avg_stay)
    else:
        avg_stay = 0
    return avg_stay

def validate_ava(restaurant, day, start_time, end_time):
    """This method validates the restaurant opening hours 

    Args:
        restaurant (restaurant): the actual restaurant
        availabilities (Availabilities): already present restaurant opening hours
        day (String):
        start_time (time): opening hour
        end_time (time): closing hour

    Returns:
        Boolean: True if the opening hours has been added correctly otherwise returns false 
    """
    availabilities = restaurant.availabilities
    rest_id = restaurant.id
    present = False
    if end_time > start_time:
        for ava in availabilities:
            if ava.day == day:
                ava.set_times(start_time, end_time)
                RestaurantAvailabilityManager.update_availability(ava)
                present = True
        if not present:
            time = RestaurantAvailability(rest_id, day, start_time, end_time)
            RestaurantAvailabilityManager.create_availability(time)
        return True
    else:
        return False