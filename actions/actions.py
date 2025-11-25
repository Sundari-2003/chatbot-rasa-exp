from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import mysql.connector


def get_connection():
    """Reusable MySQL DB connection."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sundari@2003",
        database="bank_bot"
    )


class ActionCheckBalance(Action):

    def name(self) -> Text:
        return "action_check_balance"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # 1️⃣ Retrieve customer_name slot
        customer_name = tracker.get_slot("customer_name")

        # Slot empty? Ask user again
        if not customer_name:
            dispatcher.utter_message(text="Please tell me the customer name.")
            return []

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            # 2️⃣ Query: Case insensitive match
            sql = "SELECT balance FROM customers WHERE LOWER(name)=LOWER(%s)"
            cursor.execute(sql, (customer_name,))
            result = cursor.fetchone()

            # 3️⃣ Respond
            if result:
                balance = result["balance"]
                dispatcher.utter_message(
                    text=f"{customer_name}'s balance is ${balance}"
                )
            else:
                dispatcher.utter_message(text="Customer not found in database.")

        except Exception as e:
            dispatcher.utter_message(text="Database error occurred.")
            print("[ERROR] MySQL:", str(e))

        finally:
            cursor.close()
            conn.close()

        return []





# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
