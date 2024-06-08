class UtilHolder:
    out_messages = []
    add_message_flag = False

def add_out_message(msg: str):
    UtilHolder.out_messages.append(msg)
    UtilHolder.add_message_flag = True