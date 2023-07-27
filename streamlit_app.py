import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Favourites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale Spinach and Rocket smoothie')
streamlit.text('🐔 Hard-Boiled Free Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie🥝🍇')


#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

# Display the table on the page.
streamlit.dataframe(my_fruit_list)



# Pick fruits to be included
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display table on top page
streamlit.dataframe(fruits_to_show)

#create repeatable code block(called function)
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized



#New section for api response
streamlit.header("Fruityvice Fruit Advice!")
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
   if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
   else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)

except URLError as e:
    streamlit.error()
    

#allow end user to add fruit to function def
streamlit.header("View our Fruit List - Add your Favourites")
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute ("select * from fruit_load_list")
         return my_cur.fetchall()

#Add button to load fruit
if streamlit.button('Get Fruit List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows = get_fruit_load_list()
   my_cnx.close()
   streamlit.dataframe(my_data_rows)

#allow user to add fruit
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("Insert into fruit_load_list values ('" + new_fruit +"')")
         return "Thanks for adding " +new_fruit

        
#add button to load fruit
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(back_from_function)

#add button to load fruit
#if streamlit.button('Get fruit List'):
 #   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  #  my_data_rows = get_fruit_load_list()
   # my_cnx.close()
    #streamlit.dataframe(my_data_rows)








#import requests
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)


# write your own comment -what does the next line do? 
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
#streamlit.dataframe(fruityvice_normalized)


streamlit.header("The fruit load list contains:")
#snowflake-related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("select * from fruit_load_list")
         return my_cur.fetchall()

#Add button load to fruit
if streamlit.button('Get Fruit Load List'):
   my_cnx =  snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows = get_fruit_load_list()
   streamlit.dataframe(my_data_rows)


