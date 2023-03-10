import customtkinter

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


def get_surnames():
    with connection.cursor() as cursor:
        cursor.execute("SELECT f_id, f_val FROM fam")
        surnames = cursor.fetchall()
        # delete all spaces after each surname and save f_id and f_val
        surnames = [(surname[0], surname[1].strip()) for surname in surnames]
        return surnames


def get_names():
    with connection.cursor() as cursor:
        cursor.execute("SELECT n_id, n_val FROM names")
        names = cursor.fetchall()
        # delete all spaces after each name and save n_id and n_val
        names = [(name[0], name[1].strip()) for name in names]
        return names


def get_otchestva():
    with connection.cursor() as cursor:
        cursor.execute("SELECT o_id, o_value FROM otch")
        otchestva = cursor.fetchall()
        # delete all spaces after each otchestvo and save o_id and o_value
        otchestva = [(otchestvo[0], otchestvo[1].strip())
                     for otchestvo in otchestva]
        return otchestva


def get_streets():
    with connection.cursor() as cursor:
        cursor.execute("SELECT s_id, s_val FROM street")
        streets = cursor.fetchall()
        # delete all spaces after each street and save s_id and s_val
        streets = [(street[0], street[1].strip()) for street in streets]
        return streets


# ui
# Setting the appearance mode to dark
customtkinter.set_appearance_mode("dark")

# Setting the default color theme to dark-blue
customtkinter.set_default_color_theme("dark-blue")

# Creating the main window
root = customtkinter.CTk()
root.geometry("1280x720")
root.title("Telephone Directory")

# Creating a frame inside the main window
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Creating a label inside the main window
label = customtkinter.CTkLabel(
    master=frame, text="Telephone Directory", font=("roboto", 24))
label.pack(pady=12, padx=10)

# do a dropdown menu of surnames
selected_surname = customtkinter.StringVar()

surname_dropdown = customtkinter.CTkComboBox(master=frame,
                                             variable=selected_surname)
surname_dropdown.place(relx=0.1, rely=0.15)

# do a dropdown menu of names
selected_name = customtkinter.StringVar()

name_dropdown = customtkinter.CTkComboBox(master=frame,
                                          variable=selected_name)
name_dropdown.place(relx=0.33, rely=0.15)

# do a dropdown menu of otchestva
selected_otchestvo = customtkinter.StringVar()

otchestvo_dropdown = customtkinter.CTkComboBox(master=frame,
                                               variable=selected_otchestvo)
otchestvo_dropdown.place(relx=0.57, rely=0.15)

# do a dropdown menu of streets
selected_street = customtkinter.StringVar()

street_dropdown = customtkinter.CTkComboBox(master=frame,
                                            variable=selected_street)
# place it in the next row
street_dropdown.place(relx=0.8, rely=0.15)

# text field for house number
house_number = customtkinter.CTkEntry(
    master=frame, placeholder_text="House number")
house_number.place(relx=0.1, rely=0.3)

# do a text field for korpus
korpus_number = customtkinter.CTkEntry(
    master=frame, placeholder_text="Korpus")
korpus_number.place(relx=0.33, rely=0.3)

# do a text field for flat
flat_number = customtkinter.CTkEntry(master=frame, placeholder_text="Flat")
flat_number.place(relx=0.57, rely=0.3)

# do a text field for phone number
phone_number = customtkinter.CTkEntry(
    master=frame, placeholder_text="Phone number")
phone_number.place(relx=0.8, rely=0.3)


def dropdown_fill():
    selected_surname.set("Select surname")
    selected_name.set("Select name")
    selected_otchestvo.set("Select otchestvo")
    selected_street.set("Select street")

    # write into surnames variable the list of f_val from get_surnames()
    surnamesWId = get_surnames()
    surnames = []
    for surname in surnamesWId:
        surnames.append(surname[1])
    surname_dropdown.configure(values=surnames)

    # write into names variable the list of n_val from get_names()
    namesWId = get_names()
    names = []
    for name in namesWId:
        names.append(name[1])
    name_dropdown.configure(values=names)

    # write into otchestva variable the list of o_val from get_otchestva()
    otchestvaWId = get_otchestva()
    otchestva = []
    for otchestvo in otchestvaWId:
        otchestva.append(otchestvo[1])
    otchestvo_dropdown.configure(values=otchestva)

    # write into streets variable the list of s_val from get_streets()
    streetsWId = get_streets()
    streets = []
    for street in streetsWId:
        streets.append(street[1])
    street_dropdown.configure(values=streets)


dropdown_fill()


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

    # if any of the fields are empty, don't add the person
    if surname == "" or name == "" or otchestvo == "" or street == "" or house == "" or korpus == "" or flat == "" or phone == "":
        popupmsg("Fill all the fields")
        return

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

    dropdown_fill()
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


# textbox to show all the people
textbox = customtkinter.CTkTextbox(
    master=frame, width=1000, height=250, font=("Consolas", 14))
textbox.place(relx=0.5, rely=0.95, anchor="s")

peopleFounded = []
# create a button to show all the people


def show_people():
    peopleFounded.clear()
    textbox.configure(state="normal")
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM main")
        people = cursor.fetchall()

        surnames = get_surnames()
        names = get_names()
        otchestva = get_otchestva()
        streets = get_streets()

        textbox.delete(1.0, "end")
        for i in range(len(people)):
            surname = ""
            for j in range(len(surnames)):
                if surnames[j][0] == people[i][1]:
                    surname = surnames[j][1]

            name = ""
            for j in range(len(names)):
                if names[j][0] == people[i][2]:
                    name = names[j][1]

            otchestvo = ""
            for j in range(len(otchestva)):
                if otchestva[j][0] == people[i][3]:
                    otchestvo = otchestva[j][1]

            street = ""
            for j in range(len(streets)):
                if streets[j][0] == people[i][4]:
                    street = streets[j][1]

            surname = surname.ljust(15)
            name = name.ljust(15)
            otchestvo = otchestvo.ljust(17)
            street = street.ljust(20)

            spacesAfterFlat = 10 - len(str(people[i][7]))

            textbox.insert(
                "end", f"{surname} {name} {otchestvo} {street} {people[i][5]} {people[i][6]} {people[i][7]}" + spacesAfterFlat*" " + f"{people[i][8]}\n")
            peopleFounded.append([surname, name, otchestvo, street,
                                 people[i][5], people[i][6], people[i][7], people[i][8]])
    textbox.configure(state="disabled")

# create search button


def search():
    peopleFounded.clear()
    textbox.configure(state="normal")
    textbox.delete(1.0, "end")
    surname = surname_dropdown.get()
    name = name_dropdown.get()
    otchestvo = otchestvo_dropdown.get()
    street = street_dropdown.get()
    house = house_number.get()
    korpus = korpus_number.get()
    flat = flat_number.get()
    phone = phone_number.get()

    # if all the fields are empty show all people
    if surname == "Select surname" and name == "Select name" and otchestvo == "Select otchestvo" and street == "Select street" and house == "" and korpus == "" and flat == "" and phone == "":
        show_people()
        return

    with connection.cursor() as cursor:
        # get the id of the surname from fam table
        cursor.execute(f"SELECT f_id FROM fam WHERE f_val = '{surname}'")
        surname_id = cursor.fetchall()
        surname_id = surname_id[0][0] if len(surname_id) > 0 else 0

        # get the id of the name from names table
        cursor.execute(f"SELECT n_id FROM names WHERE n_val = '{name}'")
        name_id = cursor.fetchall()
        name_id = name_id[0][0] if len(name_id) > 0 else 0

        # get the id of the otchestvo from otch table
        cursor.execute(f"SELECT o_id FROM otch WHERE o_value = '{otchestvo}'")
        otchestvo_id = cursor.fetchall()
        otchestvo_id = otchestvo_id[0][0] if len(otchestvo_id) > 0 else 0

        # get the id of the street from street table
        cursor.execute(f"SELECT s_id FROM street WHERE s_val = '{street}'")
        street_id = cursor.fetchall()
        street_id = street_id[0][0] if len(street_id) > 0 else 0

        request = "SELECT * FROM main WHERE "
        request += f"fam={surname_id}" if surname != "Select surname" else ""
        request += " AND " if surname != "Select surname" and name != "Select name" else ""
        request += f"name={name_id}" if name != "Select name" else ""
        request += " AND " if (surname != "Select surname" or name !=
                               "Select name") and otchestvo != "Select otchestvo" else ""
        request += f"otchestvo={otchestvo_id}" if otchestvo != "Select otchestvo" else ""
        request += " AND " if (surname != "Select surname" or name != "Select name" or otchestvo !=
                               "Select otchestvo") and street != "Select street" else ""
        request += f"street={street_id}" if street != "Select street" else ""
        request += " AND " if (surname != "Select surname" or name != "Select name" or otchestvo !=
                               "Select otchestvo" or street != "Select street") and house != "" else ""
        request += f"dom='{house}'" if house != "" else ""
        request += " AND " if (surname != "Select surname" or name != "Select name" or otchestvo !=
                               "Select otchestvo" or street != "Select street" or house != "") and korpus != "" else ""
        request += f"korpus='{korpus}'" if korpus != "" else ""
        request += " AND " if (surname != "Select surname" or name != "Select name" or otchestvo !=
                               "Select otchestvo" or street != "Select street" or house != "" or korpus != "") and flat != "" else ""
        request += f"kvartira={flat}" if flat != "" else ""
        request += " AND " if (surname != "Select surname" or name != "Select name" or otchestvo != "Select otchestvo" or street !=
                               "Select street" or house != "" or korpus != "" or flat != "") and phone != "" else ""
        request += f"telephone='{phone}'" if phone != "" else ""
        print(request)

        cursor.execute(request)
        peopleFound = cursor.fetchall()
        if len(peopleFound) == 0:
            popupmsg("No results found")
            return

        surnames = get_surnames()
        names = get_names()
        otchestva = get_otchestva()
        streets = get_streets()

        textbox.delete(1.0, "end")
        for i in range(len(peopleFound)):
            surname = ""
            for j in range(len(surnames)):
                if surnames[j][0] == peopleFound[i][1]:
                    surname = surnames[j][1]

            name = ""
            for j in range(len(names)):
                if names[j][0] == peopleFound[i][2]:
                    name = names[j][1]

            otchestvo = ""
            for j in range(len(otchestva)):
                if otchestva[j][0] == peopleFound[i][3]:
                    otchestvo = otchestva[j][1]

            street = ""
            for j in range(len(streets)):
                if streets[j][0] == peopleFound[i][4]:
                    street = streets[j][1]

            # add person info into peopleFounded list
            peopleFounded.append([surname, name, otchestvo, street, peopleFound[i]
                                 [5], peopleFound[i][6], peopleFound[i][7], peopleFound[i][8]])

            surname = surname.ljust(15)
            name = name.ljust(15)
            otchestvo = otchestvo.ljust(17)
            street = street.ljust(20)

            spacesAfterFlat = 10 - len(str(peopleFound[i][7]))
            textbox.insert(
                "end", f"{surname} {name} {otchestvo} {street} {peopleFound[i][5]} {peopleFound[i][6]} {peopleFound[i][7]}" + spacesAfterFlat*" " + f"{peopleFound[i][8]}\n")

    textbox.configure(state="disabled")
    dropdown_fill()


search_button = customtkinter.CTkButton(
    master=frame, text="Search", command=search)
search_button.place(relx=0.33, rely=0.45)


def delete():
    global peopleFounded
    global textbox
    global connection

    if len(peopleFounded) == 0:
        popupmsg("No results found")
        return

    with connection.cursor() as cursor:
        for person in peopleFounded:

            # get the id of the surname from fam table
            cursor.execute(f"SELECT f_id FROM fam WHERE f_val = '{person[0]}'")
            surname_id = cursor.fetchall()
            surname_id = surname_id[0][0] if len(surname_id) > 0 else 0

            # get the id of the name from names table
            cursor.execute(
                f"SELECT n_id FROM names WHERE n_val = '{person[1]}'")
            name_id = cursor.fetchall()
            name_id = name_id[0][0] if len(name_id) > 0 else 0

            # get the id of the otchestvo from otch table
            cursor.execute(
                f"SELECT o_id FROM otch WHERE o_value = '{person[2]}'")
            otchestvo_id = cursor.fetchall()
            otchestvo_id = otchestvo_id[0][0] if len(otchestvo_id) > 0 else 0

            # get the id of the street from street table
            cursor.execute(
                f"SELECT s_id FROM street WHERE s_val = '{person[3]}'")
            street_id = cursor.fetchall()
            street_id = street_id[0][0] if len(street_id) > 0 else 0

            request = f"DELETE FROM main WHERE fam={surname_id} AND name={name_id} AND otchestvo={otchestvo_id} AND street={street_id} AND dom='{person[4]}' AND korpus='{person[5]}' AND kvartira={person[6]} AND telephone='{person[7]}'"
            print(request)
            cursor.execute(request)
            connection.commit()

            # delete person surname from fam table if it is not used anymore
            cursor.execute(f"SELECT * FROM main WHERE fam={surname_id}")
            surname_id_used = cursor.fetchall()
            if len(surname_id_used) == 0:
                cursor.execute(f"DELETE FROM fam WHERE f_id={surname_id}")
                connection.commit()

            # delete person name from names table if it is not used anymore
            cursor.execute(f"SELECT * FROM main WHERE name={name_id}")
            name_id_used = cursor.fetchall()
            if len(name_id_used) == 0:
                cursor.execute(f"DELETE FROM names WHERE n_id={name_id}")
                connection.commit()

            # delete person otchestvo from otch table if it is not used anymore
            cursor.execute(
                f"SELECT * FROM main WHERE otchestvo={otchestvo_id}")
            otchestvo_id_used = cursor.fetchall()
            if len(otchestvo_id_used) == 0:
                cursor.execute(f"DELETE FROM otch WHERE o_id={otchestvo_id}")
                connection.commit()

            # delete person street from street table if it is not used anymore
            cursor.execute(f"SELECT * FROM main WHERE street={street_id}")
            street_id_used = cursor.fetchall()
            if len(street_id_used) == 0:
                cursor.execute(f"DELETE FROM street WHERE s_id={street_id}")
                connection.commit()

    textbox.configure(state="normal")
    textbox.delete(1.0, "end")
    textbox.configure(state="disabled")

    peopleFounded = []
    popupmsg("Deleted")
    dropdown_fill()


# create button to delete selected row
delete_button = customtkinter.CTkButton(
    master=frame, text="Delete", command=delete)
delete_button.place(relx=0.57, rely=0.45)


def cancel():
    # close the edit window
    global edit_window
    edit_window.destroy()


def update_person():
    # get the person from the fields update the person in the database
    global peopleFounded
    global connection
    global surname_entry, name_entry, otchestvo_entry, street_entry, dom_entry, korpus_entry, kvartira_entry, telephone_entry

    person_was = peopleFounded[0]
    person_new = [surname_entry.get(), name_entry.get(), otchestvo_entry.get(), street_entry.get(
    ), dom_entry.get(), korpus_entry.get(), kvartira_entry.get(), telephone_entry.get()]
    with connection.cursor() as cursor:
        # get the id of the surname from fam table
        cursor.execute(f"SELECT f_id FROM fam WHERE f_val = '{person_new[0]}'")
        surname_id_new = cursor.fetchall()
        if len(surname_id_new) == 0:  # if we changed the surname to an unknown one
            cursor.execute(
                f"INSERT INTO fam (f_id, f_val) VALUES (default, '{person_new[0]}')")
            connection.commit()
            cursor.execute(
                f"SELECT f_id FROM fam WHERE f_val = '{person_new[0]}'")
            surname_id_new = cursor.fetchone()[0]
        else:
            surname_id_new = surname_id_new[0][0]

        cursor.execute(f"SELECT f_id FROM fam WHERE f_val='{person_was[0]}'")
        surname_id_was = cursor.fetchone()[0]

        # get the id of the name from names table
        cursor.execute(
            f"SELECT n_id FROM names WHERE n_val = '{person_new[1]}'")
        name_id_new = cursor.fetchall()
        if len(name_id_new) == 0:  # if we changed the name to an unknown one
            cursor.execute(
                f"INSERT INTO names (n_id, n_val) VALUES (default, '{person_new[1]}')")
            connection.commit()
            cursor.execute(
                f"SELECT n_id FROM names WHERE n_val = '{person_new[1]}'")
            name_id_new = cursor.fetchone()[0]
        else:
            name_id_new = name_id_new[0][0]

        cursor.execute(f"SELECT n_id FROM names WHERE n_val='{person_was[1]}'")
        name_id_was = cursor.fetchone()[0]

        # get the id of the otchestvo from otch table
        cursor.execute(
            f"SELECT o_id FROM otch WHERE o_value = '{person_new[2]}'")
        otchestvo_id_new = cursor.fetchall()
        if len(otchestvo_id_new) == 0:  # if we changed the otchestvo to an unknown one
            cursor.execute(
                f"INSERT INTO otch (o_id, o_value) VALUES (default, '{person_new[2]}')")
            connection.commit()
            cursor.execute(
                f"SELECT o_id FROM otch WHERE o_value = '{person_new[2]}'")
            otchestvo_id_new = cursor.fetchone()[0]
        else:
            otchestvo_id_new = otchestvo_id_new[0][0]

        cursor.execute(
            f"SELECT o_id FROM otch WHERE o_value='{person_was[2]}'")
        otchestvo_id_was = cursor.fetchone()[0]

        # get the id of the street from street table
        cursor.execute(
            f"SELECT s_id FROM street WHERE s_val = '{person_new[3]}'")
        street_id_new = cursor.fetchall()
        if len(street_id_new) == 0:  # if we changed the street to an unknown one
            cursor.execute(
                f"INSERT INTO street (s_id, s_val) VALUES (default, '{person_new[3]}')")
            connection.commit()
            cursor.execute(
                f"SELECT s_id FROM street WHERE s_val = '{person_new[3]}'")
            street_id_new = cursor.fetchone()[0]
        else:
            street_id_new = street_id_new[0][0]

        cursor.execute(
            f"SELECT s_id FROM street WHERE s_val='{person_was[3]}'")
        street_id_was = cursor.fetchone()[0]

        request = f"UPDATE main SET fam={surname_id_new}, name={name_id_new}, otchestvo={otchestvo_id_new}, street={street_id_new}, dom='{person_new[4]}', korpus='{person_new[5]}', kvartira={person_new[6]}, telephone='{person_new[7]}' WHERE fam={surname_id_was} AND name={name_id_was} AND otchestvo={otchestvo_id_was} AND street={street_id_was} AND dom='{person_was[4]}' AND korpus='{person_was[5]}' AND kvartira={person_was[6]} AND telephone='{person_was[7]}'"
        print(request)
        cursor.execute(request)
        connection.commit()

        # delete the old surname from fam table if it is not used anymore
        cursor.execute(f"SELECT * FROM main WHERE fam={surname_id_was}")
        surname_id_used = cursor.fetchall()
        if len(surname_id_used) == 0:
            cursor.execute(f"DELETE FROM fam WHERE f_id={surname_id_was}")
            connection.commit()
            print("Surname deleted")

        # delete the old name from names table if it is not used anymore
        cursor.execute(f"SELECT * FROM main WHERE name={name_id_was}")
        name_id_used = cursor.fetchall()
        if len(name_id_used) == 0:
            cursor.execute(f"DELETE FROM names WHERE n_id={name_id_was}")
            connection.commit()
            print("Name deleted")

        # delete the old otchestvo from otch table if it is not used anymore
        cursor.execute(
            f"SELECT * FROM main WHERE otchestvo={otchestvo_id_was}")
        otchestvo_id_used = cursor.fetchall()
        if len(otchestvo_id_used) == 0:
            cursor.execute(f"DELETE FROM otch WHERE o_id={otchestvo_id_was}")
            connection.commit()
            print("Otchestvo deleted")

        # delete the old street from street table if it is not used anymore
        cursor.execute(f"SELECT * FROM main WHERE street={street_id_was}")
        street_id_used = cursor.fetchall()
        if len(street_id_used) == 0:
            cursor.execute(f"DELETE FROM street WHERE s_id={street_id_was}")
            connection.commit()
            print("Street deleted")

    popupmsg("Person edited successfully")
    dropdown_fill()
    cancel()


def edit():
    global peopleFounded
    global connection

    if len(peopleFounded) == 0:
        popupmsg("No results found")
        return

    if len(peopleFounded) > 1:
        popupmsg("Please select only one person")
        return

    # get the selected person
    person = peopleFounded[0]

    # get the id of the surname from fam table
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT f_id FROM fam WHERE f_val = '{person[0]}'")
        surname_id = cursor.fetchall()
        surname_id = surname_id[0][0] if len(surname_id) > 0 else 0

        # get the id of the name from names table
        cursor.execute(f"SELECT n_id FROM names WHERE n_val = '{person[1]}'")
        name_id = cursor.fetchall()
        name_id = name_id[0][0] if len(name_id) > 0 else 0

        # get the id of the otchestvo from otch table
        cursor.execute(f"SELECT o_id FROM otch WHERE o_value = '{person[2]}'")
        otchestvo_id = cursor.fetchall()
        otchestvo_id = otchestvo_id[0][0] if len(otchestvo_id) > 0 else 0

        # get the id of the street from street table
        cursor.execute(f"SELECT s_id FROM street WHERE s_val = '{person[3]}'")
        street_id = cursor.fetchall()
        street_id = street_id[0][0] if len(street_id) > 0 else 0

    # open edit window
    global edit_window
    edit_window = customtkinter.CTkToplevel()
    edit_window.title("Edit")
    edit_window.geometry("900x250")
    edit_window.resizable(False, False)

    # create frame
    edit_frame = customtkinter.CTkFrame(master=edit_window)
    edit_frame.place(relwidth=1, relheight=1)

    # create surname entry
    global surname_entry
    surname_entry = customtkinter.CTkEntry(master=edit_frame)
    surname_entry.insert(0, person[0])
    surname_entry.place(relx=0.1, rely=0.1, relwidth=0.13, relheight=0.13)

    # create name entry
    global name_entry
    name_entry = customtkinter.CTkEntry(master=edit_frame)
    name_entry.insert(0, person[1])
    name_entry.place(relx=0.33, rely=0.1, relwidth=0.13, relheight=0.13)

    # create otchestvo entry
    global otchestvo_entry
    otchestvo_entry = customtkinter.CTkEntry(master=edit_frame)
    otchestvo_entry.insert(0, person[2])
    otchestvo_entry.place(relx=0.57, rely=0.1, relwidth=0.13, relheight=0.13)

    # create street entry
    global street_entry
    street_entry = customtkinter.CTkEntry(master=edit_frame)
    street_entry.insert(0, person[3])
    street_entry.place(relx=0.8, rely=0.1, relwidth=0.13, relheight=0.13)

    # create dom entry
    global dom_entry
    dom_entry = customtkinter.CTkEntry(master=edit_frame)
    dom_entry.insert(0, person[4])
    dom_entry.place(relx=0.1, rely=0.3, relwidth=0.13, relheight=0.13)

    # create korpus entry
    global korpus_entry
    korpus_entry = customtkinter.CTkEntry(master=edit_frame)
    korpus_entry.insert(0, person[5])
    korpus_entry.place(relx=0.33, rely=0.3, relwidth=0.13, relheight=0.13)

    # create kvartira entry
    global kvartira_entry
    kvartira_entry = customtkinter.CTkEntry(master=edit_frame)
    kvartira_entry.insert(0, person[6])
    kvartira_entry.place(relx=0.57, rely=0.3, relwidth=0.13, relheight=0.13)

    # create telephone entry
    global telephone_entry
    telephone_entry = customtkinter.CTkEntry(master=edit_frame)
    telephone_entry.insert(0, person[7])
    telephone_entry.place(relx=0.8, rely=0.3, relwidth=0.13, relheight=0.13)

    # create button to save changes
    save_button = customtkinter.CTkButton(
        master=edit_frame, text="Save", command=update_person)
    save_button.place(relx=0.57, rely=0.7)

    # create button to cancel changes
    cancel_button = customtkinter.CTkButton(
        master=edit_frame, text="Cancel", command=cancel)
    cancel_button.place(relx=0.3, rely=0.7)


# create button to edit selected row
edit_button = customtkinter.CTkButton(
    master=frame, text="Edit", command=edit)
edit_button.place(relx=0.8, rely=0.45)


root.mainloop()

if connection:
    connection.close()
    print("PostgreSQL connection is closed")
