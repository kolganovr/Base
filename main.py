import customtkinter
import sys

# import libraries to connect to postrgeSQL database
import psycopg2
from psycopg2 import Error
from config import host, user, password, db_name

# Define the connection variable in the global scope
connection = None
try:
    # connect to exist database
    connection = psycopg2.connect(user=user,
                                  password=password,
                                  host=host,
                                  database=db_name)

    # get the server version
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        print(f"Server version: {cursor.fetchone()}")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)


# get the list of surnames from the database
def get_surnames():
    with connection.cursor() as cursor:
        cursor.execute("SELECT f_val FROM fam")
        surnames = cursor.fetchall()
        surnames = [surname[0] for surname in surnames]
        # delete all spaces after each surname
        surnames = [surname.strip() for surname in surnames]
        return surnames

# get the list of names from the database


def get_names():
    with connection.cursor() as cursor:
        cursor.execute("SELECT n_val FROM names")
        names = cursor.fetchall()
        names = [name[0] for name in names]
        # delete all spaces after each name
        names = [name.strip() for name in names]
        return names

# get the list of otchestva from the database


def get_otchestva():
    with connection.cursor() as cursor:
        cursor.execute("SELECT o_value FROM otch")
        otchestva = cursor.fetchall()
        otchestva = [otchestvo[0] for otchestvo in otchestva]
        # delete all spaces after each otchestvo
        otchestva = [otchestvo.strip() for otchestvo in otchestva]
        return otchestva

# get the list of streets from the database


def get_streets():
    with connection.cursor() as cursor:
        cursor.execute("SELECT s_val FROM street")
        streets = cursor.fetchall()
        streets = [street[0] for street in streets]
        # delete all spaces after each street
        streets = [street.strip() for street in streets]
        return streets


# ui
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("1280x720")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Base", font=("roboto", 24))
label.pack(pady=12, padx=10)

# do a dropdown menu of surnames
selected_surname = customtkinter.StringVar()
selected_surname.set("Select surname")

surname_dropdown = customtkinter.CTkComboBox(master=frame,
                                             variable=selected_surname, values=get_surnames())
surname_dropdown.place(relx=0.1, rely=0.15)

# do a dropdown menu of names
selected_name = customtkinter.StringVar()
selected_name.set("Select name")

name_dropdown = customtkinter.CTkComboBox(master=frame,
                                          variable=selected_name, values=get_names())
name_dropdown.place(relx=0.33, rely=0.15)

# do a dropdown menu of otchestva
selected_otchestvo = customtkinter.StringVar()
selected_otchestvo.set("Select otchestvo")

otchestvo_dropdown = customtkinter.CTkComboBox(master=frame,
                                               variable=selected_otchestvo, values=get_otchestva())
otchestvo_dropdown.place(relx=0.57, rely=0.15)

# do a dropdown menu of streets
selected_street = customtkinter.StringVar()
selected_street.set("Select street")

street_dropdown = customtkinter.CTkComboBox(master=frame,
                                            variable=selected_street, values=get_streets())
# place it in the next row
street_dropdown.place(relx=0.8, rely=0.15)

# do a text field for house number
house_number = customtkinter.CTkEntry(
    master=frame, placeholder_text="House number")
house_number.place(relx=0.1, rely=0.3)

# do a text field for korpus
korpus_number = customtkinter.CTkEntry(master=frame, placeholder_text="Korpus")
korpus_number.place(relx=0.33, rely=0.3)

# do a text field for flat
flat_number = customtkinter.CTkEntry(master=frame, placeholder_text="Flat")
flat_number.place(relx=0.57, rely=0.3)

# do a text field for phone number
phone_number = customtkinter.CTkEntry(
    master=frame, placeholder_text="Phone number")
phone_number.place(relx=0.8, rely=0.3)


# do a button to add a new person
def add_person():
    # if any of the fields are
    surname = surname_dropdown.get()
    if surname == "Select surname":
        surname = ""

    name = name_dropdown.get()
    if name == "Select name":
        name = ""

    otchestvo = otchestvo_dropdown.get()
    if otchestvo == "Select otchestvo":
        otchestvo = ""

    street = street_dropdown.get()
    if street == "Select street":
        street = ""

    house = house_number.get()
    korpus = korpus_number.get()
    flat = flat_number.get()
    phone = phone_number.get()

    with connection.cursor() as cursor:
        # if the surname is not in the database, add it
        cursor.execute(f"SELECT f_val FROM fam WHERE f_val = '{surname}'")
        surname_in_db = cursor.fetchone()
        if surname_in_db is None:
            cursor.execute(
                f"INSERT INTO fam (f_id, f_val) VALUES (default, '{surname}')")

        # get the id of the surname
        cursor.execute(f"SELECT f_id FROM fam WHERE f_val = '{surname}'")
        surname_id = cursor.fetchone()[0]

        # if the name is not in the database, add it
        cursor.execute(f"SELECT n_val FROM names WHERE n_val = '{name}'")
        name_in_db = cursor.fetchone()
        if name_in_db is None:
            cursor.execute(
                f"INSERT INTO names (n_id, n_val) VALUES (default, '{name}')")

        # get the id of the name
        cursor.execute(f"SELECT n_id FROM names WHERE n_val = '{name}'")
        name_id = cursor.fetchone()[0]

        # if the otchestvo is not in the database, add it
        cursor.execute(
            f"SELECT o_value FROM otch WHERE o_value = '{otchestvo}'")
        otchestvo_in_db = cursor.fetchone()
        if otchestvo_in_db is None:
            cursor.execute(
                f"INSERT INTO otch (o_id, o_value) VALUES (default, '{otchestvo}')")

        # get the id of the otchestvo
        cursor.execute(f"SELECT o_id FROM otch WHERE o_value = '{otchestvo}'")
        otchestvo_id = cursor.fetchone()[0]

        # if the street is not in the database, add it
        cursor.execute(f"SELECT s_val FROM street WHERE s_val = '{street}'")
        street_in_db = cursor.fetchone()
        if street_in_db is None:
            cursor.execute(
                f"INSERT INTO street (s_id, s_val) VALUES (default, '{street}')")

        # get the id of the street
        cursor.execute(f"SELECT s_id FROM street WHERE s_val = '{street}'")
        street_id = cursor.fetchone()[0]

        # insert into main values(default, 3, 3, 3, 3, '15', '1', 29, '89169735699')
        cursor.execute(
            f"INSERT INTO main VALUES (default, {surname_id}, {name_id}, {otchestvo_id}, {street_id}, '{house}', '{korpus}', {flat}, '{phone}')")

        connection.commit()

    surname_dropdown.set("Select surname")
    name_dropdown.set("Select name")
    otchestvo_dropdown.set("Select otchestvo")
    street_dropdown.set("Select street")
    house_number.delete(0, "end")
    korpus_number.delete(0, "end")
    flat_number.delete(0, "end")
    phone_number.delete(0, "end")

    popupmsg("Person added")


def popupmsg(msg):
    # animate bacgr frame to change position from rely 1.1 to rely 0.95 and then back to rely 1.1
    backgr = customtkinter.CTkFrame(
        master=frame, width=200, height=70, fg_color="#282828")
    txt = customtkinter.CTkLabel(master=backgr, text=msg, font=("Roboto", 14))
    txt.place(relx=0.5, rely=0.5, anchor="center")
    backgr.place(relx=0.5, rely=1.1, anchor="s")

    count = 0
    while count < 15:
        backgr.place_configure(rely=1.1-0.01*count)
        count += 1
        root.after(15, root.update())
    root.after(1000, root.update())
    while count > 0:
        backgr.place_configure(rely=0.95+0.01*(15-count))
        count -= 1
        root.after(15, root.update())

    backgr.destroy()


add_person_button = customtkinter.CTkButton(
    master=frame, text="Add person", command=add_person)
add_person_button.place(relx=0.1, rely=0.45)


# create a textbox to show all the people
textbox = customtkinter.CTkTextbox(master=frame, width=1000, height=250)
textbox.place(relx=0.5, rely=0.95, anchor="s")

# create a button to search for people


root.mainloop()

if connection:
    connection.close()
    print("PostgreSQL connection is closed")
