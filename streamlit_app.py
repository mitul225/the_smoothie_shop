# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!.
    """
)

#option = st.selectbox('How would you like to be contacted'
#                      , ('Email', 'Mobile', 'Phone')
#                      , label_visibility="visible")

#from snowflake.snowpark.functions import col

session = get_active_session()
df = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'))
#st.dataframe(data=df, use_container_width=True)

name_on_smoothie = st.text_input("Name on Smoothie")
itm_list = st.multiselect('Choose upto 5 fruits'
                          ,df
                          ,max_selections=5)
time_to_submit = st.button("Submit Order")

if itm_list:
    #st.write('You Selected: ',itm_list)
    ingredients_string =''
    
    for fruit_selected in itm_list:
    	ingredients_string += fruit_selected + ' '

    sql_insert_qry = """ insert into smoothies.public.orders(ingredients, name_on_order) 
        values ('""" + ingredients_string + """','""" + name_on_smoothie + """') """

    if time_to_submit:
        session.sql(sql_insert_qry).collect()
        st.success('Your Smoothie is ordered, '+name_on_smoothie+'!!!', icon="✅")

