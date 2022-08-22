import poplib
import sys


# Initialize variables
# This action is not needed in Python, but PyCharm says that the variable is not defined
# before using it. If you look at the code below, you will see that the variables are
# defined but buried within an if/then block.

server_name = ''
port_number = '995'
username = ''
password = ''


def main(my_server, my_port, my_user_name, my_password):
    try:
        # Now, we will connect and obtain the messages for the mailbox.
        mail_box = poplib.POP3_SSL(my_server, my_port)
        mail_box.user(my_user_name)
        mail_box.pass_(my_password)
        mailbox_info = mail_box.stat()

        # Once we have logged in, we now have to get the list of messages in the mailbox
        mailbox_list = mail_box.list()

        # check to see if the list was obtained. If not, we will quit. One thing to note
        # is that all the items within the mailbox list are byte-coded items. They must
        # be decoded using the UTF-8 specification to represent a string value.
        if mailbox_list[0].decode("utf-8").startswith('+OK'):

            # Now, get the list of message numbers and the message sizes.
            message_list = mailbox_list[1]
            for message_spec in message_list:
                # To delete the message, we need to supply the number (index) of the message.
                # Here we take the value in the list and convert it to a string and then an integer.
                message_number = int(message_spec.decode("utf-8").split(" ")[0])

                # Now, delete the message. The message will be flagged for deletion, and the
                # actual emails will be deleted when the quit command closes the mailbox.
                mail_box.dele(message_number)

        # Now close out the mailbox and have the mail server delete the messages.
        mail_box.quit()
    except poplib.error_proto:
        print("Unable to log on. Check to validate that your credentials are correct"
              "and try again.")
    except:
        print("Could Not get a proper connection to the email server. Ensure that the "
              "address is correct and try again.")


if __name__ == "__main__":

    # How many variables entries are in the command line entry?
    n = len(sys.argv)

    # # Now, with the count of variables in the command line entry, we will loop through
    # them to check for matches. If we find a match, we will take that variable and assign
    # it to the associated internal variable.
    for i in range(1, n):
        if sys.argv[i].startswith("servername:"):
            server_name = sys.argv[i][11:len(sys.argv[i])]
        elif sys.argv[i].startswith("portnumber:"):
            port_number = sys.argv[i][11:len(sys.argv[i])]
        elif sys.argv[i].startswith("username:"):
            username = sys.argv[i][9:len(sys.argv[i])]
        elif sys.argv[i].startswith("password:"):
            password = sys.argv[i][9:len(sys.argv[i])]
        elif sys.argv[i].startswith("help"):
            print("Help:\nThis application was written to delete all email messages"
                  "within a given Exchange\n"
                  "Server Mailbox. These deleted emails will be permanently deleted, "
                  "and will not be in the\n"
                  "mailbox's trash. Use with caution.\n\nInputs:\n"
                  "Server Name: This is the name of the server, it can be defined by"
                  " a hostname or IP address\n"
                  "Port Number: The port number that the server will be listening on.\n"
                  "User Name: The user name that can access the mailbox to be emptied.\n"
                  "Password: The password to the account.\n\n"
                  "Example:\n"
                  "$python delete_email.py servername:bob_server.com portnumber:995 "
                  "username:my_mail password:DE$%RFDS")
            exit()

    if not server_name:
        print("No Server Name defined. Exiting.")
        exit()
    elif not port_number:
        print("Invalid Port Number. Exiting.")
        exit()
    elif (not username) or (not password):
        print("Invalid User Name or Password. Exiting")
        exit()

    # Now, since we have gone through the command line variables, we will call the main routine
    # that will take the server name, port, username, and password and empty the mailbox. A good
    # thing to note is that the entries from the command line are ingested as strings. The port
    # number is an integer, so we have to cast the string as an integer for the function call.
    main(server_name, int(port_number), username, password)
