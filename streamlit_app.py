# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Streamlit app title and intro
st.title("🧃 Customize Your Smoothie!")
st.write("""
Choose the fruits you want in your custom Smoothie! 🧃
""")

# Name input
name_on_order = st.text_input('Name on Smoothie:')
st.write("The name on your Smoothie will be:", name_on_order)

# Connect to Snowflake (SniS)
cnx = st.connection("snowflake")
session = cnx.session()

# Get fruit options as a simple Python list
rows = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME")).collect()
fruit_options = [r[0] for r in rows]  # list of strings

# Multiselect widget for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_options,
    max_selections=5
)

# Only run if user selected fruits
if ingredients_list:
    # Convert list to string and escape single quotes for SQL safety
    ingredients_string = ' '.join(ingredients_list).strip().replace("'", "''")
    safe_name = (name_on_order or "").replace("'", "''")

    # Construct SQL insert statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{safe_name}')
    """

    # Button to submit
    time_to_insert = st.button('Submit Order')

    # Insert into Snowflake when clicked
    if time_to_insert:
        try:
            session.sql(my_insert_stmt).collect()
            st.success('✅ Your Smoothie has been ordered successfully!')
            # optional: clear selections / input by rerunning
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Failed to insert order: {e}")
