import urwid


def has_digit(password):
    return any(letter.isdigit() for letter in password)

def is_very_long(password):
    return len(password) > 12

def has_letters(password):
    return any(letter.isalpha() for letter in password)

def has_upper_letters(password):
    return any(letter.isupper() for letter in password)

def has_lower_letters(password):
    return any(letter.islower() for letter in password)

def has_symbol(password):
    return any(not letter.isalnum() for letter in password)


def calculate_score(password):
    score = 0
    checks = [
        has_digit,
        is_very_long,
        has_letters,
        has_upper_letters,
        has_lower_letters,
        has_symbol
    ]
    for check in checks:
        if check(password):
            score += 2
    return score


def on_ask_change(edit, new_edit_text):
    score = calculate_score(new_edit_text)
    reply.set_text(f"Рейтинг пароля: {score} из 12")


ask = urwid.Edit('Введите пароль: ', mask='*')
reply = urwid.Text("Рейтинг пароля: 0 из 12")
menu = urwid.Pile([ask, reply])
menu = urwid.Filler(menu, valign='top')

urwid.connect_signal(ask, 'change', on_ask_change)


def main():
    urwid.MainLoop(menu).run()

if __name__ == "__main__":
    main()
