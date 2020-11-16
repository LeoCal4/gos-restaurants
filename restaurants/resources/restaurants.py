from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for, jsonify)
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
        return jsonify({}), 400
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
        Linked to /restaurants/add/<id_op> [GET]
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
        return jsonify({'message': 'The Operator has added restaurant'}), 400
    list_measure = restaurant.measures.split(',')[1:]
    tables = TableManager.retrieve_by_restaurant_id(restaurant.id)
    ava = restaurant.availabilities
    avg_stay = restaurant.avg_stay

    avg_stay = convert_avg_stay_format(avg_stay)

    return jsonify({'restaurant': restaurant, 'tables': tables, 'table_form': table_form,
            'time_form': time_form, 'times': ava, 'measure_form': measure_form, 
            'avg_time_form': avg_time_form, 'avg_stay': avg_stay, 'list_measure': list_measure}), 200
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
    restaurant = RestaurantManager.retrieve_by_operator_id(id_op)

    post_data = request.get_json()
    tables_number = post_data.get('number')
    max_capacity = post_data.get('max_capacity')
    try:
        for _ in range(0, num_tables):
            table = Table(capacity=capacity, restaurant=restaurant)
            TableManager.create_table(table)
    except Exception as e:
        return jsonify({'message': 'DB ERROR\n' + e,
                        'status': 'Internal Server Error'}), 500
        
    return jsonify({'message': 'Tables successfully added'}), 200
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
    restaurant = RestaurantManager.retrieve_by_operator_id(id_op)

    post_data = request.get_json()
    try:
        day = post_data.get('day')
        start_time = post_data.get('start_time')
        end_time = post_data.get('end_time')
        restaurant = RestaurantManager.retrieve_by_id(rest_id)
        validate_ava(restaurant, day, start_time, end_time)
    except Exception as e:
        return jsonify({'message': 'Error during opening hours updating\n' + e,
                        'status': 'Bad Request'}), 400
    return jsonify({'message': 'Opening Hours updated'
                    'status': 'Success'}), 200      
    #TODO: handle the redirect
    #return redirect(url_for('restaurants.details', id_op=id_op))


# @restaurants.route('/restaurants/savemeasure/<int:id_op>/<int:rest_id>', methods=['GET', 'POST'])
# @login_required
def add_measure(id_op, rest_id):
    """This method gives the operator the possibility to add precaution meausures 
    to his restaurant
        Linked to /restaurants/save_measure/<id_op>/<rest_id> [POST]
    Args:
        id_op (int): univocal identifier of the operator
        rest_id (int): univocal identifier of the restaurant

    Returns:

    """
    restaurant = RestaurantManager.retrieve_by_operator_id(id_op)
    post_data = request.get_json()
    try:
        measure = post_data.get('measure')
        list_measure = restaurant.measures.split(',')
        measure = measure_form.data['measure']
        if measure not in list_measure:
            list_measure.append(measure)
        string = ','.join(list_measure)
        restaurant.set_measures(string)
    except Exception as e:
        return jsonify({'message': 'Error measures updating\n' + e,
                        'status': 'Bad Request'}), 400
    try:
        RestaurantManager.update_restaurant(restaurant)
    except Exception as e:
        return jsonify({'message': 'DB ERROR\n' + e,
                        'status': 'Internal Server Error'}), 500
    return jsonify({'message': 'Measure added successfully',
            'status': 'success'}), 200


# @restaurants.route('/restaurants/avgstay/<int:id_op>/<int:rest_id>', methods=['GET', 'POST'])
# @login_required
def add_avg_stay(id_op, rest_id):
    """This method gives the operator the possibility to add the average
    stay time to his restaurant
        Linked to /restaurants/save_avg_time/<id_op>/<rest_id> [POST]
    Args:
        id_op (int): univocal identifier of the operator
        rest_id (int): univocal identifier of the restaurant

    Returns:

    """
    avg_time_form = StayTimeForm()
    restaurant = RestaurantManager.retrieve_by_operator_id(id_op)
    post_data = request.get_json()
    try:
        hours = post_data.get('hours')
        minute = post_data.get('minutes')
        minute = (hours * 60) + minute
        restaurant.set_avg_stay(minute)
        RestaurantManager.update_restaurant(restaurant)
    except Exception as e:
        return jsonify({'message': 'Error during avg stay updating\n' + e,
                        'status': 'Internal Server Error'}), 500        
    return jsonify({'message': 'Average stay time successfully added'}), 200
    # return redirect(url_for('restaurants.details', id_op=id_op))


def post_edit_restaurant(id_op, rest_id):
    """This method allows the operator to edit the information about his restaurant
        Linked to /edit_restaurant/<id_op>/<rest_id> [POST]
    Args:
        id_op (int): univocal identifier of the operator
        rest_id (int): univocal identifier of the restaurant

    Returns:
        
    """
    form = RestaurantForm()
    restaurant = RestaurantManager.retrieve_by_id(rest_id)

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
        return jsonify({'message': 'Restaurant correctly modified'}), 200
        # return redirect(url_for('auth.operator', id=id_op))
    return jsonify({}), 400
    # return render_template('update_restaurant.html', form=form)

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
        raise ValueError