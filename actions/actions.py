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

        customer_name = tracker.get_slot("customer_name")

        if not customer_name:
            dispatcher.utter_message(text="Please tell me the customer name.")
            return []

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            sql = "SELECT balance FROM customers WHERE LOWER(name)=LOWER(%s)"
            cursor.execute(sql, (customer_name,))
            result = cursor.fetchone()

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


# ⭐ NEW FEATURE: Check Account Type
class ActionCheckAccountType(Action):

    def name(self) -> Text:
        return "action_check_account_type"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        customer_name = tracker.get_slot("customer_name")

        if not customer_name:
            dispatcher.utter_message(text="Please tell me the customer name.")
            return []

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            sql = "SELECT account_type FROM customers WHERE LOWER(name)=LOWER(%s)"
            cursor.execute(sql, (customer_name,))
            result = cursor.fetchone()

            if result:
                acc_type = result["account_type"]
                dispatcher.utter_message(
                    text=f"{customer_name} has a {acc_type} account."
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


class ActionCheckLastTransaction(Action):

    def name(self) -> Text:
        return "action_check_last_transaction"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # 1️⃣ Get slot value
        customer_name = tracker.get_slot("customer_name")

        if not customer_name:
            dispatcher.utter_message(text="Please tell me the customer name.")
            return []

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            # Case-insensitive search
            sql = "SELECT last_transaction FROM customers WHERE LOWER(name)=LOWER(%s)"
            cursor.execute(sql, (customer_name,))
            result = cursor.fetchone()

            if result:
                last_txn = result["last_transaction"]
                dispatcher.utter_message(
                    text=f"{customer_name}'s last transaction was: {last_txn}"
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

