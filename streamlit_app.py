import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg') 
streamlit.text('🥑🍞 Avocado Toast')   
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
preselect = ['Avocado','Strawberries']
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), preselect )
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

# fruityvice
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
  return pandas.json_normalize(fruityvice_response.json())

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    streamlit.dataframe(get_fruityvice_data(fruit_choice))
except URLError as e:
  streamlit.error()
streamlit.write('The user entered ', fruit_choice)

# snowflake
streamlit.header("View Our Fruit List - Add Your Favorites!")
def get_fruit_load_list():
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_cur = my_cnx.cursor()
  my_cur.execute("SELECT * from fruit_load_list")
  res = my_cur.fetchall()
  my_cnx.close()
  return res

if streamlit.button('Get Fruit Load List'):
  streamlit.dataframe(get_fruit_load_list())

# add fruit to snowflake
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values (' "+ new_fruit +" ')")
    return 'Thanks for adding'+new_fruit
    
fruit_suggestion = streamlit.text_input('What fruit would you like to add?','jackfruit')
if streamlit.button('Add a Fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  streamlit.write(insert_row_snowflake(fruit_suggestion))
  my_cnx.close()

