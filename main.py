import streamlit as st
from pymongo import MongoClient
from bson import ObjectId

#Database Connection class for MongoDB
class DatabaseConnection:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="Bentego"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    #Fetch data from the specified collection based on user_id
    def fetch_data(self, collection_name, user_id):
        collection = self.db[collection_name]
        try:
            user_object_id = ObjectId(user_id)
            data = collection.find_one({"_id": user_object_id})
            return data
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return None

    #Insert a new document into the specified collection
    def insert_new_document(self, collection_name, attributes):
        collection = self.db[collection_name]
        try:
            new_id = ObjectId()
            attributes["_id"] = new_id
            collection.insert_one(attributes)
            st.write(f"Inserted new document with _id: {new_id}")
        except Exception as e:
            st.error(f"Error inserting new document: {e}")

    #Delete a document from the specified collection based on user_id
    def delete_document(self, collection_name, user_id):
        collection = self.db[collection_name]
        try:
            user_object_id = ObjectId(user_id)
            result = collection.delete_one({"_id": user_object_id})
            if result.deleted_count > 0:
                st.success(f"Document with _id: {user_id} has been deleted.")
            else:
                st.warning(f"No document found with _id: {user_id}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    #Update a document in the specified collection based on user_id
    def update_document(self, collection_name, user_id, attributes):
        collection = self.db[collection_name]
        try:
            user_object_id = ObjectId(user_id)
            result = collection.update_one({"_id": user_object_id}, {"$set": attributes})
            if result.matched_count > 0:
                st.success(f"Document with _id: {user_id} has been updated.")
            else:
                st.warning(f"No document found with _id: {user_id}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    #Close the MongoDB connection
    def close_connection(self):
        self.client.close()
        st.write("MongoDB connection closed.")

#Main function to run the Streamlit app
def main():
    st.title("Heart Disease Prediction Database Interface (Bentego)")
    db_connection = DatabaseConnection()

    #Create tabs for different database operations
    tabs = st.tabs(["Insert Data", "Fetch Data", "Update Data", "Delete Data"])

    #Insert Data tab
    with tabs[0]:
        st.header("Insert Data")
        collection_name = st.text_input("Collection Name (Insert)", key="insert_collection_name")

        if collection_name:
            #Form to input attributes for new document
            attributes = {
                "Age": st.number_input("Age", min_value=0),
                "Sex": st.selectbox("Sex", options=[0, 1]),
                "Chest pain type": st.number_input("Chest pain type", min_value=1, max_value=4),
                "BP": st.number_input("BP", min_value=0),
                "Cholesterol": st.number_input("Cholesterol", min_value=0),
                "FBS over 120": st.selectbox("FBS over 120", options=[0, 1]),
                "EKG results": st.number_input("EKG results", min_value=0, max_value=2),
                "Max HR": st.number_input("Max HR", min_value=0),
                "Exercise angina": st.selectbox("Exercise angina", options=[0, 1]),
                "ST depression": st.number_input("ST depression", min_value=0.0, step=0.1),
                "Slope of ST": st.number_input("Slope of ST", min_value=1, max_value=3),
                "Number of vessels fluro": st.number_input("Number of vessels fluro", min_value=0),
                "Thallium": st.number_input("Thallium", min_value=3, max_value=7),
                "Heart Disease": st.selectbox("Heart Disease", options=["Absence", "Presence"])
            }

            #Button to insert data
            if st.button("Insert Data"):
                db_connection.insert_new_document(collection_name, attributes)
        else:
            st.error("Please enter a collection name.")

    #Fetch Data tab
    with tabs[1]:
        st.header("Fetch Data")
        collection_name = st.text_input("Collection Name (Fetch)", key="fetch_collection_name")
        user_id = st.text_input("User ID")

        if st.button("Fetch Data"):
            if collection_name and user_id:
                #Fetch data based on collection name and user ID
                data = db_connection.fetch_data(collection_name, user_id)
                if data:
                    st.write("Query results:")
                    st.json(data)
                else:
                    st.write("No data found for the given User ID.")
            else:
                st.error("Please enter both collection name and user ID.")

    #Update Data tab
    with tabs[2]:
        st.header("Update Data")
        collection_name = st.text_input("Collection Name (Update)", key="update_collection_name")
        user_id = st.text_input("User ID (Update)")

        with st.form(key="update_form"):
            fetch_button = st.form_submit_button(label="Fetch Data for Update")
            if fetch_button:

                if collection_name and user_id:
                    #Fetch data for the user to be updated
                    data = db_connection.fetch_data(collection_name, user_id)
                    if data:

                        #Form to update attributes
                        age = st.number_input("Age (Update)", min_value=0, value=data.get("Age", 0), key="update_age")
                        sex = st.selectbox("Sex (Update)", options=[0, 1], index=data.get("Sex", 0), key="update_sex")
                        chest_pain = st.number_input("Chest pain type (Update)", min_value=1, max_value=4, value=data.get("Chest pain type", 1), key="update_chest_pain")
                        bp = st.number_input("BP (Update)", min_value=0, value=data.get("BP", 0), key="update_bp")
                        cholesterol = st.number_input("Cholesterol (Update)", min_value=0, value=data.get("Cholesterol", 0), key="update_cholesterol")
                        fbs = st.selectbox("FBS over 120 (Update)", options=[0, 1], index=data.get("FBS over 120", 0), key="update_fbs")
                        ekg = st.number_input("EKG results (Update)", min_value=0, max_value=2, value=data.get("EKG results", 0), key="update_ekg")
                        max_hr = st.number_input("Max HR (Update)", min_value=0, value=data.get("Max HR", 0), key="update_max_hr")
                        angina = st.selectbox("Exercise angina (Update)", options=[0, 1], index=data.get("Exercise angina", 0), key="update_angina")
                        st_depression = st.number_input("ST depression (Update)", min_value=0.0, step=0.1, value=data.get("ST depression", 0.0), key="update_st_depression")
                        st_slope = st.number_input("Slope of ST (Update)", min_value=1, max_value=3, value=data.get("Slope of ST", 1), key="update_st_slope")
                        vessels_fluro = st.number_input("Number of vessels fluro (Update)", min_value=0, value=data.get("Number of vessels fluro", 0), key="update_vessels_fluro")
                        thallium = st.number_input("Thallium (Update)", min_value=3, max_value=7, value=data.get("Thallium", 3), key="update_thallium")
                        heart_disease = st.selectbox("Heart Disease (Update)", options=["Absence", "Presence"], index=["Absence", "Presence"].index(data.get("Heart Disease", "Absence")), key="update_heart_disease")
                    else:
                        st.write("No data found for the given User ID.")
                else:
                    st.error("Please enter both collection name and user ID.")

            update_button = st.form_submit_button(label="Update Data")
            if update_button:
                if collection_name and user_id:
                    #Prepare attributes for update
                    attributes = {
                        "Age": st.session_state.update_age,
                        "Sex": st.session_state.update_sex,
                        "Chest pain type": st.session_state.update_chest_pain,
                        "BP": st.session_state.update_bp,
                        "Cholesterol": st.session_state.update_cholesterol,
                        "FBS over 120": st.session_state.update_fbs,
                        "EKG results": st.session_state.update_ekg,
                        "Max HR": st.session_state.update_max_hr,
                        "Exercise angina": st.session_state.update_angina,
                        "ST depression": st.session_state.update_st_depression,
                        "Slope of ST": st.session_state.update_st_slope,
                        "Number of vessels fluro": st.session_state.update_vessels_fluro,
                        "Thallium": st.session_state.update_thallium,
                        "Heart Disease": st.session_state.update_heart_disease
                    }

                    #Update document in the database
                    db_connection.update_document(collection_name, user_id, attributes)
                else:
                    st.error("Please enter both collection name and user ID.")

    #Delete Data tab
    with tabs[3]:
        st.header("Delete Data")
        collection_name = st.text_input("Collection Name (Delete)", key="delete_collection_name")
        user_id = st.text_input("User ID (Delete)")

        if st.button("Delete Data"):
            if collection_name and user_id:
                #Delete document from the database
                db_connection.delete_document(collection_name, user_id)
            else:
                st.error("Please enter both collection name and user ID.")

    if st.button("Close Connection"):
        db_connection.close_connection()

# Run the main function
if __name__ == "__main__":
    main()
