from flask import render_template, redirect, request, flash, get_flashed_messages
from app import app
from app.entities import *
from app.forms import CreateUserForm
import random


title = "Space Trader"
fuel_cost = 0
next_region = ''
price_of_item = 10
primary_user = User()
primary_game = Game()
game_universe = Universe()
difficulty = ''


@app.route('/')
def start():
    return render_template('startPage.html', title=title)


@app.route('/config', methods=['GET', 'POST'])
def config_post():
    form = CreateUserForm()
    # print('we here, is the form validated? : ' + str(form.is_valid))
    # print('we here, is the form validatedDWADAWAWD? : ' + str(form.validate()))
    if request.method == 'POST':
        if form.validate():
            primary_user.set_name(form.name.data)
            primary_user.set_pilot_skill(form.pilot_skill.data)
            primary_user.set_fighter_skill(form.fighter_skill.data)
            primary_user.set_merchant_skill(form.merchant_skill.data)
            primary_user.set_engineer_skill(form.engineer_skill.data)
            difficulty = form.difficulty.data
            primary_game.set_difficulty(difficulty)
            primary_game.start_game(primary_user, game_universe)

            # Present the confirm popup, if user selects no then cancel, if the user selects yes then redirect to success
            return redirect('/liveGame')  # change back to success
        else:
            # TODO: Make it clearer to the user what part of their data is
            #  not valid. (i.e. use the raise validation errors we have
            #  right now to show them somehow
            flash("Invalid input. Make sure your name is made up of "
                  "letters (A-Z) and that your skills are numbers less "
                  "than your max skill count.")

    error_messages = ""
    print(get_flashed_messages())
    if get_flashed_messages():
        error_messages = get_flashed_messages()[0]
    return render_template('configPage.html', form=form, title="Character Configuration", user=primary_user,
                           flash_message=error_messages)


@app.route('/success')
def success():
    return render_template('successPage.html',
                           title=title, user=primary_user)


@app.route('/liveGame', methods=['GET', 'POST'])
def liveGame():
    global fuel_cost
    global next_region
    print("stuff")
    print(request.form)
    error_message = ""
    npc_encounter = ''
    if request.method == 'POST':
        if 'submit' in request.form:
            print(request.form)
            action = request.form['submit']
            npc_encounter = request.form['encounter_type']
            action = action.lower()
            if npc_encounter == 'trader':
                trader_action(action)
            elif npc_encounter == 'police':
                police_action(action)
            elif npc_encounter == 'bandit':
                raider_action(action)
            print("here" + action)
            print("there" + npc_encounter)

        elif request.form.__len__() > 1:
            next_region = request.form['region']
            fuel_cost = request.form['fuel_cost']

            # Check to see if ship has enough fuel for traveling (or if they even wanna travel?)
            if next_region != primary_user.get_region().name:
                if int(primary_user.get_ship().get_current_fuel()) >= int(fuel_cost):
                    # if primary_user.get_ship().use_fuel(fuel_cost):
                    print("we need to process the NPC encounter here")
                    npc_encounter = processEncounter(next_region)
                        
                else:
                    error_message = "You are too low on fuel!"
        elif 'buy' in request.form:
            item_bought = request.form['buy']
            if item_bought == 'fuel':
                ship = primary_user.get_ship()
                cost = ((16 - int(primary_user.get_merchant_skill())) / 16) * (
                        ship.get_fuel_cap() - ship.get_current_fuel())
                ship.fill_tank()
                primary_user.set_credits(primary_user.get_credits() - cost)
            else:
                market = primary_user.get_region().get_market()
                for item in market.get_current_cargo():
                    if item.get_name() == item_bought:
                        if item.get_cargo_space() > 0:
                            primary_user.get_ship().add_cargo(item.get_name(), 1, item.get_price())
                            item.set_cargo_space(item.get_cargo_space() - 1)
                            primary_user.set_credits(primary_user.get_credits() - item.get_price())
                            break
        elif 'sell' in request.form:
            item_sold = request.form['sell']
            ship = primary_user.get_ship()
            for item in ship.get_current_cargo():
                if item.get_name() == item_sold:
                    if item.get_cargo_space() > 0:
                        ship.remove_cargo(item.get_name(), 1)
                        primary_user.set_credits(primary_user.get_credits() + item.get_price())
    # Check to see if the user has enough money to buy

    return render_template('liveGame.html',
                           title=title, user=primary_user, universe=game_universe, game=primary_game,
                           error_message=error_message, market=primary_user.get_region().get_market(),
                           ship=primary_user.get_ship(), encounter=npc_encounter)


def raider_action(action):
    global next_region
    global fuel_cost
    print("we see a bandit and we chose to " + action)
    flee = action == "flee"
    fight = action == "fight"
    pay = action == 'pay'
    if flee:  # flee = if they choose to flee
        potential = (int(primary_user.get_pilot_skill()) + 1) * 10
        if potential < random.randint(1, 100):
            print("success flee")
        else:
            print("failed flee")
            primary_user.set_credits(0)
            primary_user.get_ship().take_damage(20)
    elif fight:  # fight = if they choose to fight
        potential = (int(primary_user.get_fighter_skill()) + 1) * 10
        print(potential)
        if potential < random.randint(1, 100):
            print("fight won")
            primary_user.set_credits(primary_user.get_credits() + random.randint(1, 100))
            for region in game_universe.get_region_list():
                if region.get_name() == next_region:
                    next_region = region
                    print(next_region)
                    if next_region != primary_user.get_region():
                        primary_user.set_region(next_region)
                        primary_user.get_ship().use_fuel(fuel_cost)

            return 'success'
        else:
            # fight lost
            print("fight lost")
            primary_user.set_credits(0)
            primary_user.get_ship().take_damage(20)
            return 'failure'
    elif pay:
        demand = primary_user.get_credits() / random.randint(2, 10) * 2.5
        print("bandit demand is ", demand)
        if primary_user.get_credits() < demand:
            # Give all Items
            if primary_user.get_ship().get_cargo_space() == 0:
                print("dwaadw")
                primary_user.get_ship().take_damage(20)
            else:
                print("wowowo")
                primary_user.get_ship().remove_all_cargo()
        else:
            primary_user.set_credits(primary_user.get_credits() - demand)

        for region in game_universe.get_region_list():
            if region.get_name() == next_region:
                next_region = region
                print(next_region)
                if next_region != primary_user.get_region():
                    primary_user.set_region(next_region)
                    primary_user.get_ship().use_fuel(fuel_cost)


def police_action(action):
    global fuel_cost
    global next_region
    print("we see a police and we chose to " + action)
    flee = action == "flee"
    fight = action == "fight"
    if flee:  # flee = if they choose to flee
        potential = (int(primary_user.get_pilot_skill()) + 1) * 10
        if potential < random.randint(1, 100):
            # success flee
            print("success")
        else:
            # fail flee
            cargo = primary_user.get_ship().get_cargo_space
            primary_user.get_ship().remove_cargo(cargo[0], 1)
            primary_user.get_ship().take_damage(40)
            primary_user.set_credits(primary_user.get_credits() - random.randint(1, 100))
    elif fight:  # fight = if they choose to fight
        potential = (int(primary_user.get_fighter_skill()) + 1) * 10
        if potential < random.randint(1, 100):
            # success fight
            for region in game_universe.get_region_list():
                if region.get_name() == next_region:
                    next_region = region
                    print(next_region)
                    if next_region != primary_user.get_region():
                        primary_user.set_region(next_region)
                        primary_user.get_ship().use_fuel(fuel_cost)
        else:
            # fail fight
            primary_user.get_ship().take_damage(30)
    else:  # user chooses to ignore
        # give up item
        cargo = primary_user.get_ship().get_cargo()
        primary_user.get_ship().remove_cargo(cargo[0], 1)
        primary_user.get_ship().remove_cargo("GRATTT", 1)
        for region in game_universe.get_region_list():
            if region.get_name() == next_region:
                next_region = region
                print(next_region)
                if next_region != primary_user.get_region():
                    primary_user.set_region(next_region)
                    primary_user.get_ship().use_fuel(fuel_cost)


def trader_action(action):
    global fuel_cost
    global next_region
    global price_of_item
    print("we see a trader and we chose to " + action)
    buy = action == 'buy'
    ignore = action == "flee" or action == "ignore"
    fight = action == "fight"
    negotiate = action == 'negotiate'
    if buy:  # buy = if they choose to buy
        primary_user.get_ship().add_cargo("Boo boo sticks", 1, price_of_item)
        print(primary_user.get_ship().get_cargo_space())
        primary_user.set_credits(primary_user.get_credits() - price_of_item)
        for region in game_universe.get_region_list():
            if region.get_name() == next_region:
                next_region = region
                print(next_region)
                if next_region != primary_user.get_region():
                    primary_user.set_region(next_region)
                    primary_user.get_ship().use_fuel(fuel_cost)
    elif ignore:  # ignore = if they choose to ignore and move on
        for region in game_universe.get_region_list():
            if region.get_name() == next_region:
                next_region = region
                print(next_region)
                if next_region != primary_user.get_region():
                    primary_user.set_region(next_region)
                    primary_user.get_ship().use_fuel(fuel_cost)
    elif fight:  # fight = if they choose to fight
        # fight em
        potential = (int(primary_user.get_fighter_skill()) + 1) * 10
        if potential < random.randint(1, 80):
            # win fight
            print("fight won")
            primary_user.get_ship().add_cargo("GRATTT", 2, random.randint(1, 50))
        else:
            # lost fight
            print("fight lost")
            primary_user.get_ship().take_damage(20)
            for region in game_universe.get_region_list():
                if region.get_name() == next_region:
                    next_region = region
                    print(next_region)
                    if next_region != primary_user.get_region():
                        primary_user.set_region(next_region)
                        primary_user.get_ship().use_fuel(fuel_cost)

    elif negotiate:  # negotiate
        potential = (int(primary_user.get_merchant_skill()) + 1) * 10
        if potential < random.randint(1, 100):
            # price goes down
            # price_of_item = price_of_item / 2
            primary_user.get_ship().add_cargo("Boo boo sticks", 1, (price_of_item / 2))
            primary_user.set_credits(primary_user.get_credits() - (price_of_item / 2))
        else:
            price_of_item += random.randint(1, 50)


def processEncounter(next_region, action=""):
    # Random Encounters
    factor = 0
    if difficulty == 'easy':
        factor = 10
    elif difficulty == 'medium':
        factor = 25
    elif difficulty == 'hard':
        factor = 35

    if factor <= random.randint(1, 100):
        # Start encounter, higher rate of encounters with higher difficulties
        print("an encounter occurred")
        rand = random.randint(1, 100)
        # Therefore causing the player to encounter police and bandits at higher
        # difficulties more often
        if rand > 40:
            return 'bandit'
        elif rand > 10 and primary_user.get_ship().get_capacity() != 0:
            # Police
            return 'police'
            print("a police appeared")
        else:
            # Trader
            print("a trader appeared")
            return 'trader'

def refuel_action(action): #check if they have enough money, and if their ship's fuel is below 100
    print("Refueling ship!")
    price = 0
    if difficulty == 'easy':
        price = 5
    elif difficulty == 'medium':
        price = 10
    elif difficulty == 'hard':
        price = 15

    primary_user.get_ship().fill_tank(10) #add 10 to tank
    primary_user.set_credits(primary_user.get_credits() - price)

def repair_action(action): #check if they have enough money, and if their ship's health is below 100
    print("Repairing ship!")
    price = 0
    if difficulty == 'easy':
        price = 5
    elif difficulty == 'medium':
        price = 10
    elif difficulty == 'hard':
        price = 15
    
    price = int(price / (int(primary_user.get_engineer_skill()) + 1) * 1.5)
    repair = 5 * (int(primary_user.get_engineer_skill()) + 1)

    primary_user.get_ship().repair(repair)
    primary_user.set_credits(primary_user.get_credits() - price)

