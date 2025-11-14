# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Streamlit app title and intro
st.title("🧃 Customize Your Smoothie!")
st.write("""
Choose the fruits you want in your custom Smoothie! 🧃
""")

# Name input
name_on_order = st.text_input('Name on Smoothie:')
st.write("The name on your Smoothie will be:", name_on_order)

# Get Snowflake session and data
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Multiselect widget for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe ,
    max_selections=5
    
)

# Only run if user selected fruits
if ingredients_list:
    # Convert list to string
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # Construct SQL insert statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string.strip()}', '{name_on_order}')
    """

    #st.write("SQL to execute:")
    #st.code(my_insert_stmt)
    #st.stop()

    # Button to submit
    time_to_insert = st.button('Submit Order')

    # Insert into Snowflake when clicked
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('✅ Your Smoothie has been ordered successfully!')

