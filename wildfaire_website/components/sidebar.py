import streamlit as st
from components.geocoding import geocode_address

## function to populate data entry sidebar
def sidebar():
    with st.sidebar:
        ## basic markdown instructions
        st.markdown(
            "How to use WildfAIire: \n"
            "1. Enter your address\n"
            "2. WildfAIre will return information \n"
                "on wildfires in your loction"
        )

        def form_callback():
            st.write(1+1)
            #st.write(st.session_state)

        with st.form(key='address'):
            ##address details to be submitted to geocoding API
            street = st.text_input('Street', key='my_street')
            town = st.text_input('Town', key='my_town')
            state = st.text_input('State/County', key='my_county')
            zip = st.text_input('ZIP/Postcode', key='my_postcode')
            country = st.selectbox('Country', ['France', 'United Kingdom', 'United States'], key='my_country')
            address_to_geocode = f"{street},{town},{state},{country}"
            submit_button = st.form_submit_button(label="Submit", on_click=form_callback)



    # Every form must have a submit button.


    #        if submitted:
    #            st.write(st.session_state['address'])
    #            geocode_address(st.write(st.session_state['address']))
