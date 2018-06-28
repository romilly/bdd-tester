from microbit import *
import radio

__version__=1.29
ROUND_OVER = 'round over'
TEAM = 'team'
CHECKING_IN = 'checking in'
RUNNER = 'runner'
THATS_ALL_FOLKS = "that's all, folks!"
CHECK_IN = 'check in'
ALL_IN = 'all checked in'
DONE = -1
button_c = pin8
button_d = pin16

radio.on()
scores = {}
team = 1
round = 1


def say(text):
    print(text)
    display.scroll(text)


def wait_for_role():
    while True:
        if button_a.is_pressed():
            say(RUNNER)
            return RUNNER
        message = radio.receive()
        if message == CHECK_IN:
            print(TEAM)
            return TEAM


def wait_for_checkins():
    global team
    radio.send(CHECK_IN)
    while True:
        if button_b.is_pressed():
            say(ALL_IN)
            radio.send(ALL_IN)
            return
        message = radio.receive()
        if message == CHECKING_IN:
            scores[team] = 0
            radio.send('%s: %d' % (TEAM, team))
            say('team %d checked in' % team)
            team += 1


def check_answer(message):
        say(message)
        (ignore, number, buzz) = message.split()
        while True:
            if button_a.is_pressed():
                scores[int(number)] += 1
                return DONE
            if button_b.is_pressed():
                return


def wait_for_end():
    while True:
        quit_if_game_over()
        # end round
        if button_c.read_digital():
            return DONE
        message = radio.receive()
        if message is None:
            continue
        response = check_answer(message)
        if response == DONE:
            return DONE


# TODO: replace global scores with local parameter
def run_a_round():
    # get rid of late buzzes
    while radio.receive():
        pass
    say('round %d' % round)
    radio.send('round')
    wait_for_end()
    round_over()


def round_over():
    global round
    round = round + 1
    radio.send(ROUND_OVER)
    say(ROUND_OVER)


def quit_if_game_over():
    if pin16.read_digital():
        goodbye()


def run_the_quiz():
    say('Play time!')
    while True:
        quit_if_game_over()
        run_a_round()
        round_over()


def check_in():
    say(CHECKING_IN)
    while True:
        radio.receive() # clear other teams' messages
        if button_b.is_pressed():
            say('check')
            radio.send(CHECKING_IN)
            break
    while True:
        message = radio.receive()
        if message is None:
            continue
        say(message)
        if message.startswith(TEAM):
            (ignore, number) = message.split(':')
            return int(number)


def play_a_round(team):
    while True:
        message = radio.receive()
        if message == ROUND_OVER:
            say(ROUND_OVER)
            return
        if button_a.is_pressed():
            radio.send('%s %d buzzing' % (TEAM, team))
            say('team %d buzzing' % team)


def are_we_finished():
    message = radio.receive()
    if message is None:
        return None
    if message.startswith(THATS_ALL_FOLKS):
        parts = message.split()
        for part in parts[1:]:
            team, their_score = part.split(':')
            scores[int(team)] = int(their_score)
    return scores


def play_the_quiz(team):
    display.scroll('starting quiz')
    while True:
        result =  are_we_finished()
        if result is not None:
            return result
        display.scroll('playing round')
        play_a_round(team)


def goodbye():
    message = THATS_ALL_FOLKS
    for team in scores.keys():
        message += ' %d:%d' % (team, scores[team])
    radio.send(message)
    reset() # quit this run and start again


def run():
    print(__version__)
    role = wait_for_role()
    if role == RUNNER:
        do_runner_things()
    if role == TEAM:
        do_team_player_things()
    show_results()


def wait_for_start():
    while True:
        message = radio.receive()
        if message is None:
            continue
        if message == ALL_IN:
            return


def do_team_player_things():
    my_team = check_in()
    wait_for_start()
    # say('team %d' % my_team)
    play_the_quiz(my_team)


def do_runner_things():
    wait_for_checkins()
    run_the_quiz()
    goodbye()


def show_results():
    say('scores ')
    sleep(1)
    for team in scores.keys():
        say(' %d:%d' % (team, scores[team]))

run()


    

