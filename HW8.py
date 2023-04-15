# Your name: Abby Lee
# Your student id: 6619 1622
# Your email: abbylee@umich.edu
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute('SELECT name, category_id, building_id, rating FROM restaurants')
    rows = cur.fetchall()

    restaurant_data = {}
    for row in rows:
        name = row[0]
        category_id = row[1]
        building_id = row[2]
        rating = row[3]

        cur.execute('SELECT category FROM categories WHERE id = ?', (category_id,))
        category = cur.fetchone()[0]
        cur.execute('SELECT building FROM buildings WHERE id = ?', (building_id,))
        building = cur.fetchone()[0]

        info = {
            'category': category,
            'building': building,
            'rating': rating
        }
        restaurant_data[name] = info

    con.close()
    return restaurant_data


def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute('''SELECT category, COUNT(*) 
                   FROM restaurants 
                   JOIN categories ON category_id = categories.id 
                   GROUP BY category''')
    rows = cur.fetchall()

    rest_categories = {}
    for row in rows:
        category = row[0]
        count = row[1]
        rest_categories[category] = count 

    con.close()

    categories = list(rest_categories.keys())
    all_counts = list(rest_categories.values())

    plt.barh(categories, all_counts)
    plt.xlabel('Number of Restaurants') 
    plt.ylabel('Restaurant Categories')
    plt.title('Types of Restaurant on South University Ave')
    plt.show()

    return rest_categories

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute('''SELECT name
                   FROM restaurants 
                   JOIN buildings ON building_id = buildings.id 
                   WHERE building = ? 
                   ORDER BY restaurants.rating DESC''', (building_num,))
    rows = cur.fetchall()

    rest_names = [row[0] for row in rows]

    return rest_names

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute('''SELECT categories.category, ROUND(AVG(restaurants.rating), 1) 
                   FROM restaurants 
                   JOIN categories ON restaurants.category_id = categories.id 
                   GROUP BY category
                   ORDER BY AVG(restaurants.rating) DESC''')
    category_rows = cur.fetchall()

    category_names = [row[0] for row in category_rows]
    category_avg_ratings = [row[1] for row in category_rows]

    cur.execute('''SELECT buildings.building, ROUND(AVG(restaurants.rating), 1) 
                   FROM restaurants 
                   JOIN buildings ON restaurants.building_id = buildings.id 
                   GROUP BY buildings.building
                   ORDER BY AVG(restaurants.rating) DESC''')
    building_rows = cur.fetchall()

    building_numbers = [row[0] for row in building_rows]
    building_avg_ratings = [row[1] for row in building_rows]

    con.close()

    highest_category = (category_names[0], category_avg_ratings[0])
    highest_building = (building_numbers[0], building_avg_ratings[0])


    plt.figure((8,8))
    plt.subplot(2, 1, 1)
    plt.barh(category_names, category_avg_ratings)
    plt.xlabel('Ratings')
    plt.ylabel('Categories')
    plt.title('Average Restaurant Rating by Category')
    plt.xlim(0, 5)

    plt.subplot(2, 1, 2)
    plt.barh(building_numbers, building_avg_ratings)
    plt.xlabel('Rating')
    plt.ylabel('Buildings')
    plt.title('Average Restaurant Rating by Building')
    plt.xlim(0, 5)

    plt.show()

    return [highest_category, highest_building] 

#Try calling your functions here
def main():
    load_rest_data('South_U_Restaurants.db')
    plot_rest_categories('South_U_Restaurants.db')
    find_rest_in_building(1140, 'South_U_Restaurants.db')
    get_highest_rating('South_U_Restaurants.db')


class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
